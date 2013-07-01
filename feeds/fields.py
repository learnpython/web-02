# -*- coding: utf-8 -*-

import inspect

from django.db import models

from south.modelsinspector import add_introspection_rules
from picklefield.fields import PickledObjectField


class LazyFieldMixin(object):
    '''
    Примесь, позволяющая отложить для классов-полей преобразование БД -> питон
    до первого к ним обращения. Это может быть полезно, если обращение к полю
    происходит только в редких случаях, а преобразование занимает много
    ресурсов (память, время, процессор, соединение с сетью, ...).
    '''
    pass  # TODO


class DenormalizedFieldMixin(object):
    '''
    Общие свойства полей для хранения денормализованных данных. Значения таких
    полей нельзя редактиовать с помощью форм, а также передавать на сторону
    БД при сохранении объекта. Поменять значения таких полей можно только
    через метод update queryset'a. Где будет этот update - это уже другой
    вопрос. Некоторые поля можно устанавливать при сохранении своей модели,
    некоторые - чужой, а еще некоторые - в обработчиках сигналов. Названия
    таких полей в модели должно начинаться с символа _, а доступ к ним лучше
    делать с помощью соответствующих свойств без символа _. Эта примесь, а
    также логика работы с такими полями, не есть что-то универсальное, что
    потом можно будет использовать в другом проекте. Для этого нужно сделать
    что-то типа DenormalizedModelMixin. Если будут такие пожелания, можно
    попробовать это сделать.
    '''
    def __init__(self, *args, **kwargs):
        kwargs = kwargs.copy()
        for option_name, default_value in (('blank', True),
                                           ('null', True),
                                           ('default', None),
                                           ('editable', False)):
            if option_name not in kwargs:
                kwargs[option_name] = default_value

        super(DenormalizedFieldMixin, self).__init__(*args, **kwargs)


class DenormalizedDictField(LazyFieldMixin,
                            DenormalizedFieldMixin,
                            PickledObjectField):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class DenormalizedCharField(DenormalizedFieldMixin, models.CharField):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class DenormalizedDateTimeField(DenormalizedFieldMixin, models.DateTimeField):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


# учим south работать с нашими полями
local_symbols = locals()
for name in dir():
    value = local_symbols[name]

    if inspect.isclass(value) and issubclass(value, DenormalizedFieldMixin):
        regexp = u'^%s.%s$' % (value.__module__, value.__name__)
        regexp = regexp.replace('.', '\.')
        add_introspection_rules([], [regexp])
