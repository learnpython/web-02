# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('chitatel_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('href', self.gf('django.db.models.fields.URLField')(unique=True, max_length=255)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'feeds', ['Feed'])

        # Adding model 'Entry'
        db.create_table('chitatel_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['feeds.Feed'])),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'feeds', ['Entry'])

        # Adding unique constraint on 'Entry', fields ['feed', 'uid']
        db.create_unique('chitatel_entry', ['feed_id', 'uid'])

        # Adding model 'Tag'
        db.create_table('chitatel_tag', (
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32, primary_key=True)),
        ))
        db.send_create_signal(u'feeds', ['Tag'])


    def backwards(self, orm):
        # Removing unique constraint on 'Entry', fields ['feed', 'uid']
        db.delete_unique('chitatel_entry', ['feed_id', 'uid'])

        # Deleting model 'Feed'
        db.delete_table('chitatel_feed')

        # Deleting model 'Entry'
        db.delete_table('chitatel_entry')

        # Deleting model 'Tag'
        db.delete_table('chitatel_tag')


    models = {
        u'feeds.entry': {
            'Meta': {'unique_together': "(('feed', 'uid'),)", 'object_name': 'Entry', 'db_table': "'chitatel_entry'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['feeds.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['feeds']