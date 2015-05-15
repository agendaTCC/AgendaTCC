# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Splash'
        db.create_table(u'website_splash', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('texto', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('exibir_noticias', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exibir_texto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exibir_imagens', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'website', ['Splash'])

        # Adding model 'Imagens'
        db.create_table(u'website_imagens', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('entrada', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('texto', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('exibir', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('splash', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Splash'])),
        ))
        db.send_create_signal(u'website', ['Imagens'])


    def backwards(self, orm):
        # Deleting model 'Splash'
        db.delete_table(u'website_splash')

        # Deleting model 'Imagens'
        db.delete_table(u'website_imagens')


    models = {
        u'website.imagens': {
            'Meta': {'object_name': 'Imagens'},
            'data': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entrada': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'exibir': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'splash': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Splash']"}),
            'texto': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'website.splash': {
            'Meta': {'object_name': 'Splash'},
            'data': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exibir_imagens': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exibir_noticias': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exibir_texto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'texto': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['website']