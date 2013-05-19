# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Sound.nature'
        db.alter_column('collection_sound', 'nature_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collection.Nature'], null=True))

        # Changing field 'Sound.completude'
        db.alter_column('collection_sound', 'completude_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collection.Completude'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Sound.nature'
        raise RuntimeError("Cannot reverse this migration. 'Sound.nature' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Sound.completude'
        raise RuntimeError("Cannot reverse this migration. 'Sound.completude' and its values cannot be restored.")

    models = {
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
        'collection.sound': {
            'Meta': {'object_name': 'Sound'},
            'completude': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collection.Completude']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collection.Nature']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sound': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['collection']