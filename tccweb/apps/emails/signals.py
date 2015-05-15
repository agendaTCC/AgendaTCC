from django.db.models.signals import post_save
from models import EnviaEmail
from emails.sendmail import send_emails

def emailSignal(sender,**kw):
	instance = kw["instance"]
	if kw["created"]:
		send_emails(instance.filtro, instance.departamento, instance.assunto, instance.corpo)

# post_save.connect(emailSignal, sender=EnviaEmail, dispatch_uid="emails-EnviaEmails-signal")