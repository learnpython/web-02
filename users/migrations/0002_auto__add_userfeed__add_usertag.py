# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserFeed'
        db.create_table('chitatel_users_feeds', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Feed'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_tags', null=True, to=orm['users.UserTag'])),
        ))
        db.send_create_signal(u'users', ['UserFeed'])

        # Adding model 'UserTag'
        db.create_table('chitatel_users_tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_tags', to=orm['feeds.Tag'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_tags', to=orm['users.User'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tags', null=True, to=orm['users.UserTag'])),
        ))
        db.send_create_signal(u'users', ['UserTag'])

        # Removing M2M table for field feeds on 'User'
        db.delete_table(db.shorten_name('chitatel_user_feeds'))

        # Removing M2M table for field tags on 'User'
        db.delete_table(db.shorten_name('chitatel_user_tags'))


    def backwards(self, orm):
        # Deleting model 'UserFeed'
        db.delete_table('chitatel_users_feeds')

        # Deleting model 'UserTag'
        db.delete_table('chitatel_users_tags')

        # Adding M2M table for field feeds on 'User'
        m2m_table_name = db.shorten_name('chitatel_user_feeds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False)),
            ('feed', models.ForeignKey(orm[u'feeds.feed'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'feed_id'])

        # Adding M2M table for field tags on 'User'
        m2m_table_name = db.shorten_name('chitatel_user_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False)),
            ('tag', models.ForeignKey(orm[u'feeds.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'tag_id'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'feeds.feed': {
            'Meta': {'object_name': 'Feed', 'db_table': "'chitatel_feed'"},
            'href': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'feeds.tag': {
            'Meta': {'object_name': 'Tag', 'db_table': "'chitatel_tag'"},
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User', 'db_table': "'chitatel_user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'to': u"orm['feeds.Feed']", 'through': u"orm['users.UserFeed']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'to': u"orm['feeds.Tag']", 'through': u"orm['users.UserTag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'users.userfeed': {
            'Meta': {'object_name': 'UserFeed', 'db_table': "'chitatel_users_feeds'"},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feeds.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_tags'", 'null': 'True', 'to': u"orm['users.UserTag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'users.usertag': {
            'Meta': {'object_name': 'UserTag', 'db_table': "'chitatel_users_tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tags'", 'null': 'True', 'to': u"orm['users.UserTag']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_tags'", 'to': u"orm['feeds.Tag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_tags'", 'to': u"orm['users.User']"})
        }
    }

    complete_apps = ['users']