# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Repository.url'
        db.alter_column('grepo_base_repository', 'url', self.gf('django.db.models.fields.URLField')(max_length=255))

        # Changing field 'Repository.created_at'
        db.alter_column('grepo_base_repository', 'created_at', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Repository.updated_at'
        db.alter_column('grepo_base_repository', 'updated_at', self.gf('django.db.models.fields.DateField')())


    def backwards(self, orm):
        
        # Changing field 'Repository.url'
        db.alter_column('grepo_base_repository', 'url', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Repository.created_at'
        db.alter_column('grepo_base_repository', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Repository.updated_at'
        db.alter_column('grepo_base_repository', 'updated_at', self.gf('django.db.models.fields.DateTimeField')())


    models = {
        'grepo_base.language': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'grepo_base.repository': {
            'Meta': {'ordering': "['-score', 'updated_at']", 'object_name': 'Repository'},
            'created_at': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'repositories'", 'symmetrical': 'False', 'to': "orm['grepo_base.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'score': ('django.db.models.fields.FloatField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.SmallIntegerField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['grepo_base']
