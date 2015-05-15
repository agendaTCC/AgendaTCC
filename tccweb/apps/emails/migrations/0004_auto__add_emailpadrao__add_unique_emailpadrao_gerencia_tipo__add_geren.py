# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailPadrao'
        db.create_table(u'emails_emailpadrao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gerencia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emails.GerenciarEmails'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('cco', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('corpo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'emails', ['EmailPadrao'])

        # Adding unique constraint on 'EmailPadrao', fields ['gerencia', 'tipo']
        db.create_unique(u'emails_emailpadrao', ['gerencia_id', 'tipo'])

        # Adding model 'GerenciarEmails'
        db.create_table(u'emails_gerenciaremails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['departamentos.Departamento'])),
        ))
        db.send_create_signal(u'emails', ['GerenciarEmails'])


    def backwards(self, orm):
        # Removing unique constraint on 'EmailPadrao', fields ['gerencia', 'tipo']
        db.delete_unique(u'emails_emailpadrao', ['gerencia_id', 'tipo'])

        # Deleting model 'EmailPadrao'
        db.delete_table(u'emails_emailpadrao')

        # Deleting model 'GerenciarEmails'
        db.delete_table(u'emails_gerenciaremails')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cursos.curso': {
            'Meta': {'object_name': 'Curso'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['departamentos.Departamento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'departamentos.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'cor': ('departamentos.models.ColorField', [], {'max_length': '10', 'blank': 'True'}),
            'docentes_responsaveis': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'docentes_responsaveis_pelo_grupo'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['usuarios._User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'watermark': ('django.db.models.fields.files.FileField', [], {'default': "'/home/pumba/Django_Projects/tccweb/tccweb/tccweb/media/img/generico.gif'", 'max_length': '100'})
        },
        u'emails.emailpadrao': {
            'Meta': {'unique_together': "(('gerencia', 'tipo'),)", 'object_name': 'EmailPadrao'},
            'cco': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'corpo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gerencia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emails.GerenciarEmails']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'emails.enviaemail': {
            'Meta': {'object_name': 'EnviaEmail'},
            'assunto': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'corpo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['departamentos.Departamento']"}),
            'enviada_em': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'filtro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'emails.gerenciaremails': {
            'Meta': {'object_name': 'GerenciarEmails'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['departamentos.Departamento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'usuarios._user': {
            'Meta': {'object_name': '_User'},
            'aluno': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cep': ('django.db.models.fields.CharField', [], {'default': "'00000-000'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'cidade': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'complemento': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cpf': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'curso'", 'null': 'True', 'to': u"orm['cursos.Curso']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'docente': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'doutorando': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'mestrando': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'monitor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nome_completo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'numero_usp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pae': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'secretario': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supervisor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tel': ('django.db.models.fields.CharField', [], {'default': "'(00)0000-0000'", 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'uf': ('django.db.models.fields.CharField', [], {'default': "'SP'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['emails']