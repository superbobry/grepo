# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing M2M table for field language on 'Repository'
        db.delete_table('grepo_base_repository_language')

        # Adding M2M table for field languages on 'Repository'
        db.create_table('grepo_base_repository_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repository', models.ForeignKey(orm['grepo_base.repository'], null=False)),
            ('language', models.ForeignKey(orm['grepo_base.language'], null=False))
        ))
        db.create_unique('grepo_base_repository_languages', ['repository_id', 'language_id'])


    def backwards(self, orm):
        
        # Adding M2M table for field language on 'Repository'
        db.create_table('grepo_base_repository_language', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repository', models.ForeignKey(orm['grepo_base.repository'], null=False)),
            ('language', models.ForeignKey(orm['grepo_base.language'], null=False))
        ))
        db.create_unique('grepo_base_repository_language', ['repository_id', 'language_id'])

        # Removing M2M table for field languages on 'Repository'
        db.delete_table('grepo_base_repository_languages')


    models = {
        'grepo_base.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'grepo_base.repository': {
            'Meta': {'object_name': 'Repository'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'repositories'", 'symmetrical': 'False', 'to': "orm['grepo_base.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'score': ('django.db.models.fields.FloatField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.SmallIntegerField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['grepo_base']
