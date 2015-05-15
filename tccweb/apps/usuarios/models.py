# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from cursos.models import Curso

UF = (
      ('AC','AC'),
      ('AP','AP'),
      ('AM','AM'),
      ('BA','BA'),
      ('CE','CE'),
      ('DF','DF'),
      ('ES','ES'),
      ('GO','GO'),
      ('MA','MA'),
      ('MT','MT'),
      ('MS','MS'),
      ('MG','MG'),
      ('PA','PA'),
      ('PB','PB'),
      ('PR','PR'),
      ('PE','PE'),
      ('PI','PI'),
      ('RJ','RJ'),
      ('RN','RN'),
      ('RS','RS'),
      ('RO','RO'),
      ('RR','RR'),
      ('SC','SC'),
      ('SP','SP'),
      ('SE','SE'),
      ('TO','TO'),
                )
class _UserManager(BaseUserManager):

    def _create_user(self, cpf, password,email,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not cpf:
            raise ValueError('Campo CPF Vazio')
        email = self.normalize_email(email)
        user = self.model(cpf = cpf,email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, cpf, email,password=None, **extra_fields):
        return self._create_user(cpf, password, email,False, False,
                                 **extra_fields)

    def create_superuser(self, cpf, password, email,**extra_fields):
        return self._create_user(cpf, password, email,False, False,
                                 **extra_fields)   


   
class _User(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(_(u'CPF'), max_length=11, unique=True)
    email = models.EmailField(_(u'E-mail'), max_length=254 , null = True, blank = True)
    nome_completo = models.CharField(_(u'Nome'), max_length=255, blank=True)
    numero_usp = models.IntegerField(_(u'Número USP'),null=True, blank=True)
    curso  = models.ForeignKey(Curso,related_name = 'curso', null = True, blank = True)
    endereco = models.CharField(_(u'Endereço'),max_length=255, null = True, blank = True)
    numero = models.IntegerField(_(u'Número'),max_length=4, null = True, blank = True)
    complemento = models.CharField(_(u'Complemento'),max_length=255, null = True, blank = True)
    cidade = models.CharField(_(u'Cidade'),max_length=255, null = True, blank = True)
    uf = models.CharField(_(u'UF'),max_length = 2,default = 'SP',  null = True, blank = True, choices = UF)
    bairro = models.CharField(_(u'Bairro'),max_length= 255, null = True, blank = True)
    tel = models.CharField(_(u'Telefone'),max_length=15,default='(00)0000-0000', null = True, blank = True)
    cep = models.CharField(_(u'CEP'),max_length=10, default='00000-000', null = True, blank = True)

    docente = models.BooleanField(_(u'Docente'), default=False,
        help_text=_(u'Indica se Usuario é Docente.'))
    doutorando = models.BooleanField(_(u'Aluno de Doutorado'), default=False,
        help_text=_(u'Indica se Usuario é Aluno de Doutorado.'))
    mestrando = models.BooleanField(_(u'Aluno de Mestrado'), default=False,
        help_text=_(u'Indica se Usuario é Aluno de Mestrado.'))
    aluno = models.BooleanField(_(u'Aluno'), default=True,
        help_text=_(u'Indica se Usuario é aluno de graduação.'))
    funcionario = models.BooleanField(_(u'Funcionario não Docente'), default=False,
        help_text=_(u'Indica se Usuario é Funcionário não Docente.'))
    monitor = models.BooleanField(_(u'Monitor'), default=False,
        help_text=_(u'Indica se Usuario é Monitor.'))
    pae = models.BooleanField(_(u'Estagiario PAE'), default=False,
        help_text=_(u'Indica se Usuario é Estagiario PAE.'))
    supervisor = models.BooleanField(_(u'Supervisor'), default=False,
        help_text=_(u'Indica se Usuario é Supervisor.'))
    secretario = models.BooleanField(_(u'Secretário'), default=False,
        help_text=_(u'Indica se Usuario é Secretário.'))

    is_staff = models.BooleanField(_(u'Pertence a administração'), default=False,
        help_text=_(u'Usuario tem autorização para acessar a administração.'))
    is_active = models.BooleanField(_('Ativo'), default=True,
        help_text=_(u'Estatus do Usuario.'))
    

    date_joined = models.DateTimeField(_(u'Data de Cadastro'), default=timezone.now)

    objects = _UserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = [email,nome_completo,]

    class Meta:
        verbose_name = _(u'usuário')
        verbose_name_plural = _(u'usuário')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.cpf)

    def get_full_name(self):
        full_name = self.nome_completo
        return full_name.strip()

    def get_short_name(self):
        full_name = self.nome_completo
        return full_name.strip()

    def email_user(self, subject, message, from_email=None):
        msg = EmailMessage(subject, message, from_email, [self.email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

    def __unicode__(self):
        return self.nome_completo
    def empresa(self):
        if self.supervisor:
            return self.empresa_set.all()
        return None

class UsuarioAutorizado(models.Model):
  email = models.EmailField(_(u'E-mail'), max_length=254 , null = True, blank = True, unique=True)
  nome_completo = models.CharField(_(u'Nome'), max_length=255, blank=True)
  numero_usp = models.CharField(_(u'Número USP'),max_length=10,unique=True)

  class Meta:
      verbose_name = _(u'Usuário Autorizado')
      verbose_name_plural = _(u'Usuários Autorizados')

  def __unicode__(self):
      return self.nome_completo

class CSVUsuario(models.Model):
    class Meta:
        verbose_name = 'Adicionar via CSV'
        verbose_name_plural = 'Adicionar via CSV'
    file = models.FileField(upload_to='tmp')
    log = models.TextField(verbose_name='log', null = True, blank = True)
    criada_em = models.DateTimeField(auto_now_add=True,verbose_name='Data da criação')
    def __unicode__(self):
        return  self.criada_em.strftime('%d de %B de %Y as %H:%M')