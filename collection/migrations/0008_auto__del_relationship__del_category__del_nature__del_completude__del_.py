# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Relationship'
        db.delete_table('collection_relationship')

        # Deleting model 'Category'
        db.delete_table('collection_category')

        # Deleting model 'Nature'
        db.delete_table('collection_nature')

        # Deleting model 'Completude'
        db.delete_table('collection_completude')

        # Deleting field 'Sound.description'
        db.delete_column('collection_sound', 'description')

        # Deleting field 'Sound.short_name'
        db.delete_column('collection_sound', 'short_name')

        # Deleting field 'Sound.nature'
        db.delete_column('collection_sound', 'nature_id')

        # Deleting field 'Sound.category'
        db.delete_column('collection_sound', 'category_id')

        # Deleting field 'Sound.completude'
        db.delete_column('collection_sound', 'completude_id')


    def backwards(self, orm):
        # Adding model 'Relationship'
        db.create_table('collection_relationship', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collection.Category'])),
            ('sound', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collection.Sound'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('collection', ['Relationship'])

        # Adding model 'Category'
        db.create_table('collection_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('collection', ['Category'])

        # Adding model 'Nature'
        db.create_table('collection_nature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('collection', ['Nature'])

        # Adding model 'Completude'
        db.create_table('collection_completude', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('collection', ['Completude'])

        # Adding field 'Sound.description'
        db.add_column('collection_sound', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Sound.short_name'
        db.add_column('collection_sound', 'short_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Sound.nature'
        db.add_column('collection_sound', 'nature',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collection.Nature'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sound.category'
        db.add_column('collection_sound', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collection.Category'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sound.completude'
        db.add_column('collection_sound', 'completude',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collection.Completude'], null=True, blank=True),
                      keep_default=False)


    models = {
        'collection.sound': {
            'Meta': {'object_name': 'Sound'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sound': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['collection']