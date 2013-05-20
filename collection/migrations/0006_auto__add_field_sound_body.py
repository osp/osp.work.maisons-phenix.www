# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Sound.body'
        db.add_column('collection_sound', 'body',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Sound.body'
        db.delete_column('collection_sound', 'body')


    models = {
        'collection.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'collection.completude': {
            'Meta': {'object_name': 'Completude'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'collection.nature': {
            'Meta': {'object_name': 'Nature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'collection.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collection.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sound': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collection.Sound']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'collection.sound': {
            'Meta': {'object_name': 'Sound'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collection.Category']", 'null': 'True', 'blank': 'True'}),
            'completude': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collection.Completude']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collection.Nature']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sound': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'foo_set'", 'symmetrical': 'False', 'through': "orm['collection.Relationship']", 'to': "orm['collection.Category']"})
        }
    }

    complete_apps = ['collection']