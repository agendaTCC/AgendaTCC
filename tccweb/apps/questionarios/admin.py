from django.contrib import admin
from models import Questionario, Perguntas, Respostas, QuestionarioRespondido


class PerguntasAdmin(admin.TabularInline):
    model = Perguntas

class QuestionarioAdmin(admin.ModelAdmin):
    inlines = [PerguntasAdmin]

class RespostasAdmin(admin.TabularInline):
	can_delete = False
	extra = 0
	editable_fields = []
	ordering = ("pergunta__numero",)
	def get_readonly_fields(self, request, obj=None):
		fields = []
		for field in self.model._meta.get_all_field_names():
			if (not field == 'id'):
				if (field not in self.editable_fields):
					fields.append(field)
		return fields

	def has_add_permission(self, request):
		return False
	model = Respostas

class QuestionarioRespondidoAdmin(admin.ModelAdmin):
	inlines = [RespostasAdmin]
	list_display = ('get_aluno_display', 'questionario', 'get_tipo_display', 'get_departamento_display')
	list_filter = ('questionario__tipo', 'questionario__departamento', 'projeto__disciplina__semestre')
	search_fields = ['projeto', 'projeto__aluno', 'projeto__disciplina']


admin.site.register(Questionario,QuestionarioAdmin)
admin.site.register(QuestionarioRespondido, QuestionarioRespondidoAdmin)