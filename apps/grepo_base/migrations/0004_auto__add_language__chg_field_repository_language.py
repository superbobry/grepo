# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Language'
        db.create_table('grepo_base_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
        ))
        db.send_create_signal('grepo_base', ['Language'])

        # Renaming column for 'Repository.language' to match new field type.
        db.rename_column('grepo_base_repository', 'language', 'language_id')
        # Changing field 'Repository.language'
        db.alter_column('grepo_base_repository', 'language_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grepo_base.Language']))

        # Adding index on 'Repository', fields ['language']
        db.create_index('grepo_base_repository', ['language_id'])


    def backwards(self, orm):
        
        # Removing index on 'Repository', fields ['language']
        db.delete_index('grepo_base_repository', ['language_id'])

        # Deleting model 'Language'
        db.delete_table('grepo_base_language')

        # Renaming column for 'Repository.language' to match new field type.
        db.rename_column('grepo_base_repository', 'language_id', 'language')
        # Changing field 'Repository.language'
        db.alter_column('grepo_base_repository', 'language', self.gf('django.db.models.fields.SmallIntegerField')())


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
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'repositories'", 'to': "orm['grepo_base.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'score': ('django.db.models.fields.FloatField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.SmallIntegerField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['grepo_base']
