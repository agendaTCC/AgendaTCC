# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Questionario'
        db.create_table(u'questionarios_questionario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'questionario_departamento', to=orm['departamentos.Departamento'])),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'questionarios', ['Questionario'])

        # Adding model 'Perguntas'
        db.create_table(u'questionarios_perguntas', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('questionario', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'perguntas_questionario', to=orm['questionarios.Questionario'])),
            ('numero', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pergunta', self.gf('django.db.models.fields.TextField')()),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='0', max_length=255, null=True, blank=True)),
            ('opcoes', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'questionarios', ['Perguntas'])

        # Adding model 'QuestionarioRespondido'
        db.create_table(u'questionarios_questionariorespondido', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('projeto', self.gf('django.db.models.fields.related.ForeignKey')(default='1', related_name='questionario_respondido_projeto', to=orm['projetos.ProjetoDeGraduacao'])),
            ('questionario', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'resposta_projeto_questionario', to=orm['questionarios.Questionario'])),
            ('data', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'questionarios', ['QuestionarioRespondido'])

        # Adding unique constraint on 'QuestionarioRespondido', fields ['projeto', 'questionario']
        db.create_unique(u'questionarios_questionariorespondido', ['projeto_id', 'questionario_id'])

        # Adding model 'Respostas'
        db.create_table(u'questionarios_respostas', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('respondido', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'resposta_respondido', to=orm['questionarios.QuestionarioRespondido'])),
            ('pergunta', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'respostas_pergunta', to=orm['questionarios.Perguntas'])),
            ('resposta', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'questionarios', ['Respostas'])


    def backwards(self, orm):
        # Removing unique constraint on 'QuestionarioRespondido', fields ['projeto', 'questionario']
        db.delete_unique(u'questionarios_questionariorespondido', ['projeto_id', 'questionario_id'])

        # Deleting model 'Questionario'
        db.delete_table(u'questionarios_questionario')

        # Deleting model 'Perguntas'
        db.delete_table(u'questionarios_perguntas')

        # Deleting model 'QuestionarioRespondido'
        db.delete_table(u'questionarios_questionariorespondido')

        # Deleting model 'Respostas'
        db.delete_table(u'questionarios_respostas')


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
            'watermark': ('django.db.models.fields.files.FileField', [], {'default': "'/var/www/html/tccweb/tccweb/tccweb/media/img/generico.gif'", 'max_length': '100'})
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
            'semestre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'disciplina_semestre'", 'to': u"orm['semestre.Semestre']"}),
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
        u'projetos.projetodegraduacao': {
            'Meta': {'object_name': 'ProjetoDeGraduacao'},
            'aluno': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projeto_aluno'", 'null': 'True', 'to': u"orm['usuarios._User']"}),
            'area': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'atividades': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cancelado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cronograma': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'descricao': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disciplina': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projeto_disciplina'", 'to': u"orm['disciplinas.Disciplina']"}),
            'espc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'justificativa': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'orientador': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projeto_orientador'", 'null': 'True', 'to': u"orm['usuarios._User']"}),
            'rascunho': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subarea': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projeto_supervisor'", 'null': 'True', 'to': u"orm['usuarios._User']"}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'validacao_docente': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'validacao_graduacao': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'validacao_supervisor_orientador': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        u'questionarios.perguntas': {
            'Meta': {'object_name': 'Perguntas'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'opcoes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pergunta': ('django.db.models.fields.TextField', [], {}),
            'questionario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'perguntas_questionario'", 'to': u"orm['questionarios.Questionario']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'questionarios.questionario': {
            'Meta': {'object_name': 'Questionario'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'questionario_departamento'", 'to': u"orm['departamentos.Departamento']"}),
            'descricao': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'questionarios.questionariorespondido': {
            'Meta': {'unique_together': "(('projeto', 'questionario'),)", 'object_name': 'QuestionarioRespondido'},
            'data': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projeto': ('django.db.models.fields.related.ForeignKey', [], {'default': "'1'", 'related_name': "'questionario_respondido_projeto'", 'to': u"orm['projetos.ProjetoDeGraduacao']"}),
            'questionario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'resposta_projeto_questionario'", 'to': u"orm['questionarios.Questionario']"})
        },
        u'questionarios.respostas': {
            'Meta': {'object_name': 'Respostas'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pergunta': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'respostas_pergunta'", 'to': u"orm['questionarios.Perguntas']"}),
            'respondido': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'resposta_respondido'", 'to': u"orm['questionarios.QuestionarioRespondido']"}),
            'resposta': ('django.db.models.fields.TextField', [], {})
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
            'inic_banca_responsavel': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'inic_inscricao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'inicio_semestre': ('django.db.models.fields.DateField', [], {}),
            'max_apresentacao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'max_autorizacao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'max_banca_alunos': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'max_banca_convidado': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'max_banca_responsavel': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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

    complete_apps = ['questionarios']