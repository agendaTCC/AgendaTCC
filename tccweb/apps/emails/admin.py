from django.contrib import admin
from django.template import RequestContext
from models import EnviaEmail, EmailPadrao , GerenciarEmails
from forms import EnviaEmailForm
from emails.sendmail import send_emails

class EnviaEmailAdmin(admin.ModelAdmin):
	change_form_template = 'admin/emails/EnviaEmail/change_form.html'
	def save_model(self, request, obj, form, changed):
		print request.POST
		if "_save_send" in request.POST:
			send_emails(obj.filtro, obj.departamento, obj.assunto, obj.corpo)
			return super(EnviaEmailAdmin, self).save_model(request, obj, form, changed)
		else:
			return super(EnviaEmailAdmin, self).save_model(request, obj, form, changed)
	
	class Media:
		js = ['/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js']
	form = EnviaEmailForm
	save_on_top = True
	list_display = (['departamento', 'enviada_em','assunto','get_filtro_display'])
	
	list_display_links = (['departamento', 'enviada_em','assunto']) 
	date_hierarchy = 'enviada_em'
	readonly_fields=('enviada_em',)

class PadraoAdmin(admin.TabularInline):
    model = EmailPadrao
    
# class AutomaticoAdmin(admin.TabularInline):
#     model = EmailAutomatico
#     form = FormAutomatico

class GerenciarEmailsAdmin(admin.ModelAdmin):
    inlines = [PadraoAdmin]
    # inlines = [PadraoAdmin,AutomaticoAdmin]
    class Media:
        js = ['/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js']

admin.site.register(EnviaEmail, EnviaEmailAdmin)
admin.site.register(GerenciarEmails,GerenciarEmailsAdmin)
