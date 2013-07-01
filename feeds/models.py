# -*- coding: utf-8 -*-

import hashlib

import feedparser

from django.db import transaction
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .fields import (DenormalizedDictField, DenormalizedFieldMixin,
                     DenormalizedCharField, DenormalizedDateTimeField)
from .managers import FeedManager, EntryManager


class FeedParserDict(models.Model):
    '''
    Абстрактная модель для хранения информации об интересующей нас части
    rss/atom-ленты. Такую информацию можно получить из результата разбора
    ленты функцией feedparser.parse(...) -> dict. Интересующую нас структуру
    храним в поле _dict, а отдельные ее элементы (к которым должен быть
    доступ со стороны ОРМ или которые будут использоваться в 90% случаях)
    добавляем как денормализованные поля в нашу модель. При изменении поля
    _dict (с помощью соответствующего свойства) каждое из таких полей
    автоматически обновляется. В дикте храним всю информацию о ленте/статье,
    которую только можно получить, а вот использовать ее или нет - выбирать
    нам. При использовании жесткой модели (создаем для каждого интересующего
    нас параметра поле в модели), в случае необходимости добавить новое св-во
    ленты, это св-во будет заполняться только для новых объектов, для
    существующих же объектов его значения нам неоткуда будет взять.
    '''
    _dict = DenormalizedDictField(_('dict'), db_column='_dict')

    class Meta:
        abstract = True

    @property
    def dict(self, default={}):
        if self._dict is not None:
            return self._dict
        else:
            return default

    @dict.setter
    def dict(self, value):
        '''
        Сохраняет значение нашего словаря в БД, а также обновляет и сохраняет
        значения всех денорм. полей.
        '''
        update_kwargs = {}

        self._dict = value
        update_kwargs['_dict'] = self._dict

        for denormalized_field in self._meta.fields:
            if denormalized_field.name in update_kwargs:
                continue

            if not isinstance(denormalized_field, DenormalizedFieldMixin):
                continue

            if not denormalized_field.name.startswith('_'):
                continue

            normalized_field_name = denormalized_field.name[1:]

            # Устанавливаем значение нашего денорм. поля в None. Это заставит
            # соответствующее ему свойство обращаться к _dict для получения
            # нового значения, а не использовать закешированное в денорм. поле.
            setattr(self, denormalized_field.name, None)

            value = getattr(self, normalized_field_name, None)
            update_kwargs[denormalized_field.name] = value
            setattr(self, denormalized_field.name, value)

        # Если есть такая возможность, то обновляем значения денорм. полей
        # в БД. Если объект еще не был сохранен, то наши денорм. поля будут
        # сохранениы всместе с другими полями при первом сохранении.
        if self.pk:
            self.__class__.objects_with_deferred_dict.filter(
                pk=self.pk
            ).update(**update_kwargs)

    def save(self, *args, **kwargs):
        # Если сохраняем объект в первый раз, то сохраняем в БД все поля, а
        # если нет, то выбрасываем все денорм. поля (они обновляются только
        # при обновления свойства dict).
        if self.pk:
            update_fields = []

            for field in self._meta.fields:
                if field.name == 'id':
                    continue

                if isinstance(field, DenormalizedFieldMixin):
                    continue

                update_fields.append(field.name)

            kwargs = kwargs.copy()
            kwargs['update_fields'] = update_fields

        # Если наш словарь не определен (содержимое ленты еще неизвестно),
        # то даем возможность денорм. полям получить какие-то нач. значения.
        if self._dict is None:
            self.dict = None  # вызываем процедуру денормализации #

        super(FeedParserDict, self).save(*args, **kwargs)

    def _get_first_not_none_value(self, _dict, keys, default=u''):
        for key in keys:
            value = _dict.get(key)

            if value is not None:
                return value

        return default


class Feed(FeedParserDict):
    '''
    Модель для хранения информации о ленте. Список свойств соответствует
    списку элементов atom-ленты, т.е. с любой лентой работаем как с
    atom-лентой. Элементы rss-ленты приводятся к элементам atom-ленты.

    Сравнение RSS и Atom:
    http://www.intertwingly.net/wiki/pie/Rss20AndAtom10Compared
    '''

    url = models.URLField(_('URL'), max_length=255, unique=True, default=u'')
    reloaded_at = models.DateTimeField(_('reloaded at'), null=True,
                                       blank=True, default=None,
                                       editable=False)
    # http://pythonhosted.org/feedparser/reference-bozo_exception.html
    bozo_exception = models.CharField(_('bozo exception'), max_length=128,
                                      null=True, blank=True, default=None,
                                      editable=False)
    _title = DenormalizedCharField(_('title'), max_length=255,
                                   db_column='_title')

    # Для того, чтобы всегда помнили о производительности и выбирали
    # тот или иной менеджер в зависимости от ситуации, название
    # менеджера по умолчанию изменено.
    objects_without_deferred_dict = models.Manager()
    objects_with_deferred_dict = FeedManager()

    class Meta:
        db_table = 'chitatel_feed'
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')

    def __init__(self, *args, **kwargs):
        super(Feed, self).__init__(*args, **kwargs)

        # Будем отслеживать изменение поля url.
        self._prev_url = self.url

    def __unicode__(self):
        return self.title

    @property
    def title(self):
        if self._title is not None:
            return self._title
        else:
            if self.is_loaded:
                return self._get_first_not_none_value(self.dict, ('title',))
            else:
                return unicode(_('Loading ...'))

    @property
    def is_loaded(self):
        return self.reloaded_at is not None

    @property
    def is_valid(self):
        return not bool(self.bozo_exception)

    def save(self, *args, **kwargs):
        # Если у нас меняется урл ленты (хотя такого допускать нельзя,
        # поскольку на одну и ту же ленту могут быть подписаны разные
        # пользователи), то сбрасываем все поля в начальное состояние.
        if self._prev_url != self.url:
            self.entries.all().delete()
            self.bozo_exception = None
            self.reloaded_at = None
            self.dict = None

        super(Feed, self).save(*args, **kwargs)

    def reload(self):
        '''
        Аналог метода save, но кроме всего прочего, загружает и парсит ленту,
        а также добавляет и обновляет статьи. Возвращает http-заголовки.
        По кеширующим заголовкам можно будет вычислить время следующего
        обновления.
        '''
        feed = feedparser.parse(self.url)
        self.reloaded_at = timezone.now()

        self.bozo_exception = feed.get('bozo_exception')
        if self.bozo_exception is None:
            self.dict = feed.feed

        super(Feed, self).save()

        # Добавляем новые статьи и обновляем старые
        for _dict in feed.entries:
            entry = Entry(feed=self, dict=_dict)

            try:
                entry.save()
            except IntegrityError:
                transaction.rollback()

                #try:
                #    entry = entry.__class__.objects_with_deferred_dict.get(
                #        feed=self, _uuid=entry._uuid
                #    )
                #
                #    entry.dict = _dict
                #except entry.__class__.DoesNotExist:
                #    pass

        return feed.get('headers')


class Entry(FeedParserDict):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'),
                             related_name='entries')
    _uuid = DenormalizedCharField(_('uuid'), max_length=255,
                                  db_column='_uuid')
    _title = DenormalizedCharField(_('title'), max_length=255,
                                   db_column='_title')
    _link = DenormalizedCharField(_('link'), max_length=255,
                                  db_column='_link')
    _published_at = DenormalizedDateTimeField(_('published at'))

    objects_without_deferred_dict = models.Manager()
    objects_with_deferred_dict = EntryManager()

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'chitatel_entry'
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        unique_together = ('feed', '_uuid')
        index_together = (('feed', '_published_at'),)
        ordering = ('-_published_at',)

    @property
    def uuid(self):
        if self._uuid is not None:
            return self._uuid
        else:
            return self._get_first_not_none_value(self.dict, ('id', 'link'))

    @property
    def title(self):
        if self._title is not None:
            return self._title
        else:
            return self._get_first_not_none_value(self.dict, ('title',))

    @property
    def link(self):
        if self._link is not None:
            return self._link
        else:
            return self._get_first_not_none_value(self.dict, ('link',))

    @property
    def published_at(self):
        if self._published_at is not None:
            return self._published_at
        else:
            value = self._get_first_not_none_value(
                self.dict, ('published_parsed',)
            )

            if not value:
                value = timezone.now()
            else:
                value = timezone.make_aware(
                    timezone.datetime(*value[:-3]), timezone.utc
                )

            return value


class Tag(models.Model):
    """
    Tag model.

    For now save here only tag name as primary key.
    """
    name = models.CharField(
        _('name'), max_length=32, primary_key=True, unique=True
    )

    class Meta:
        db_table = 'chitatel_tag'
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __unicode__(self):
        """
        Unicode representation.
        """
        return self.name


try:
    from .signals import nothing
except ImportError:
    pass
