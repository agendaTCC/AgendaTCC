from django.forms import ModelForm, Form, ModelChoiceField
from models import Disciplina
from departamentos.models import Departamento

class DisciplinaForm(ModelForm):
    class Meta:
        model = Disciplina
        exclude = ('alunos', 'monitores')
        
class Adiciona_ao_grupoform(Form):
    grupo = ModelChoiceField(queryset=Departamento.objects.all(), empty_label="(Nothing)")