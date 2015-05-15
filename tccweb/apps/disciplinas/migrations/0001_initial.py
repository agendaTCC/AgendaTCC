# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NomeDisciplina'
        db.create_table(u'disciplinas_nomedisciplina', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('ementa', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'disciplinas', ['NomeDisciplina'])

        # Adding model 'Disciplina'
        db.create_table(u'disciplinas_disciplina', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['disciplinas.NomeDisciplina'])),
            ('ano', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('turma', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('criada_em', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('semestre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['semestre.Semestre'])),
            ('esta_ativa', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'disciplinas', ['Disciplina'])

        # Adding M2M table for field alunos on 'Disciplina'
        m2m_table_name = db.shorten_name(u'disciplinas_disciplina_alunos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('disciplina', models.ForeignKey(orm[u'disciplinas.disciplina'], null=False)),
            ('_user', models.ForeignKey(orm[u'usuarios._user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['disciplina_id', '_user_id'])

        # Adding M2M table for field professores on 'Disciplina'
        m2m_table_name = db.shorten_name(u'disciplinas_disciplina_professores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('disciplina', models.ForeignKey(orm[u'disciplinas.disciplina'], null=False)),
            ('_user', models.ForeignKey(orm[u'usuarios._user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['disciplina_id', '_user_id'])

        # Adding M2M table for field monitores on 'Disciplina'
        m2m_table_name = db.shorten_name(u'disciplinas_disciplina_monitores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('disciplina', models.ForeignKey(orm[u'disciplinas.disciplina'], null=False)),
            ('_user', models.ForeignKey(orm[u'usuarios._user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['disciplina_id', '_user_id'])


    def backwards(self, orm):
        # Deleting model 'NomeDisciplina'
        db.delete_table(u'disciplinas_nomedisciplina')

        # Deleting model 'Disciplina'
        db.delete_table(u'disciplinas_disciplina')

        # Removing M2M table for field alunos on 'Disciplina'
        db.delete_table(db.shorten_name(u'disciplinas_disciplina_alunos'))

        # Removing M2M table for field professores on 'Disciplina'
        db.delete_table(db.shorten_name(u'disciplinas_disciplina_professores'))

        # Removing M2M table for field monitores on 'Disciplina'
        db.delete_table(db.shorten_name(u'disciplinas_disciplina_monitores'))


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
        u'disciplinas.disciplina': {
            'Meta': {'ordering': "['-semestre']", 'object_name': 'Disciplina'},
            'alunos': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'aluno_disciplina'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['usuarios._User']"}),
            'ano': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'criada_em': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'esta_ativa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitores': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'monitor_disciplina'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['usuarios._User']"}),
            'professores': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'professor_disciplina'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['usuarios._User']"}),
            'semestre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['semestre.Semestre']"}),
            'titulo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['disciplinas.NomeDisciplina']"}),
            'turma': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'disciplinas.nomedisciplina': {
            'Meta': {'object_name': 'NomeDisciplina'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'ementa': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'semestre.semestre': {
            'Meta': {'object_name': 'Semestre'},
            'ano': ('django.db.models.fields.IntegerField', [], {}),
            'atual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'autorizacao_mestrando': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fim_semestre': ('django.db.models.fields.DateField', [], {}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['departamentos.Departamento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inic_apresentacao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'inic_banca_alunos': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'inic_banca_convidado': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'inic_inscricao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'inicio_semestre': ('django.db.models.fields.DateField', [], {}),
            'max_apresentacao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'max_autorizacao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'max_banca_alunos': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'max_banca_convidado': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'max_inscricao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'max_titulo_areas': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'semestre': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '1'})
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

    complete_apps = ['disciplinas']