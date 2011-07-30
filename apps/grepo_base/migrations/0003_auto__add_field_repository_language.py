# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Repository.language'
        db.add_column('grepo_base_repository', 'language', self.gf('django.db.models.fields.SmallIntegerField')(default='python'), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Repository.language'
        db.delete_column('grepo_base_repository', 'language')


    models = {
        'grepo_base.repository': {
            'Meta': {'object_name': 'Repository'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.SmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'score': ('django.db.models.fields.FloatField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.SmallIntegerField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['grepo_base']
