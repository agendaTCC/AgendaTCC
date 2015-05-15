# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sala'
        db.create_table(u'salas_sala', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ativa', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'salas', ['Sala'])


    def backwards(self, orm):
        # Deleting model 'Sala'
        db.delete_table(u'salas_sala')


    models = {
        u'salas.sala': {
            'Meta': {'object_name': 'Sala'},
            'ativa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['salas']