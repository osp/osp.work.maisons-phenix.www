# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Completude'
        db.create_table('collection_completude', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('collection', ['Completude'])

        # Adding model 'Nature'
        db.create_table('collection_nature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('collection', ['Nature'])

        # Adding model 'Sound'
        db.create_table('collection_sound', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sound', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('completude', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collection.Completude'])),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('nature', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collection.Nature'])),
        ))
        db.send_create_signal('collection', ['Sound'])


    def backwards(self, orm):
        # Deleting model 'Completude'
        db.delete_table('collection_completude')

        # Deleting model 'Nature'
        db.delete_table('collection_nature')

        # Deleting model 'Sound'
        db.delete_table('collection_sound')


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
            'completude': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collection.Completude']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collection.Nature']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sound': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['collection']