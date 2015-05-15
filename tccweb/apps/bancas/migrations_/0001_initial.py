# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Banca'
        db.create_table(u'bancas_banca', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hora_inicial', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('hora_final', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('data', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='departamento', null=True, to=orm['departamentos.Departamento'])),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresa.Empresa'], null=True, blank=True)),
            ('banca_docente', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='banca1', null=True, to=orm['usuarios._User'])),
            ('banca_convidado', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='banca2', null=True, to=orm['usuarios._User'])),
            ('sala', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['salas.Sala'], null=True, blank=True)),
            ('reservada', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('alteravel', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('projeto', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'banca_projeto', null=True, to=orm['projetos.ProjetoDeGraduacao'])),
            ('cancelada', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bancas', ['Banca'])

        # Adding model 'Agenda'
        db.create_table(u'bancas_agenda', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agenda_departamento', to=orm['departamentos.Departamento'])),
            ('salas', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agenda_sala', to=orm['salas.Sala'])),
        ))
        db.send_create_signal(u'bancas', ['Agenda'])

        # Adding model 'Dia_Agenda'
        db.create_table(u'bancas_dia_agenda', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agenda', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bancas.Agenda'])),
            ('data', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('horarios', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'bancas', ['Dia_Agenda'])

        # Adding model 'Apresentacao'
        db.create_table(u'bancas_apresentacao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.DateTimeField')()),
            ('sala', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usuarios._User'])),
            ('banca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bancas.Banca'])),
        ))
        db.send_create_signal(u'bancas', ['Apresentacao'])


    def backwards(self, orm):
        # Deleting model 'Banca'
        db.delete_table(u'bancas_banca')

        # Deleting model 'Agenda'
        db.delete_table(u'bancas_agenda')

        # Deleting model 'Dia_Agenda'
        db.delete_table(u'bancas_dia_agenda')

        # Deleting model 'Apresentacao'
        db.delete_table(u'bancas_apresentacao')


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
        u'bancas.agenda': {
            'Meta': {'object_name': 'Agenda'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agenda_departamento'", 'to': u"orm['departamentos.Departamento']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salas': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agenda_sala'", 'to': u"orm['salas.Sala']"})
        },
        u'bancas.apresentacao': {
            'Meta': {'object_name': 'Apresentacao'},
            'banca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bancas.Banca']"}),
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sala': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usuarios._User']"})
        },
        u'bancas.banca': {
            'Meta': {'object_name': 'Banca'},
            'alteravel': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'banca_convidado': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'banca2'", 'null': 'True', 'to': u"orm['usuarios._User']"}),
            'banca_docente': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'banca1'", 'null': 'True', 'to': u"orm['usuarios._User']"}),
            'cancelada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'data': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'departamento'", 'null': 'True', 'to': u"orm['departamentos.Departamento']"}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empresa.Empresa']", 'null': 'True', 'blank': 'True'}),
            'hora_final': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'hora_inicial': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projeto': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'banca_projeto'", 'null': 'True', 'to': u"orm['projetos.ProjetoDeGraduacao']"}),
            'reservada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sala': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['salas.Sala']", 'null': 'True', 'blank': 'True'})
        },
        u'bancas.dia_agenda': {
            'Meta': {'object_name': 'Dia_Agenda'},
            'agenda': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bancas.Agenda']"}),
            'data': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'horarios': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'empresa.empresa': {
            'Meta': {'object_name': 'Empresa'},
            'UF': ('django.db.models.fields.CharField', [], {'default': "'SP'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'area_de_atuacao': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cep': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'cidade': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'comp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'data_final_convenio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'data_inicio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'data_inicio_convenio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'end': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome_empresarial': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nome_fantasia': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nro_inscricao': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'num': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'supervisores': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['usuarios._User']", 'null': 'True', 'blank': 'True'})
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
        u'salas.sala': {
            'Meta': {'object_name': 'Sala'},
            'ativa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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

    complete_apps = ['bancas']