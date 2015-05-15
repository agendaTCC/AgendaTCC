from django.forms import ModelForm, CheckboxSelectMultiple
from models import EntregaMonografiaRevisada, EntregaMonografiaOriginal

class EntregaMonografiaRevisadaForm(ModelForm):
    class Meta:
        model = EntregaMonografiaRevisada
        exclude = ('alunos', 'data', 'disciplina')
        
class EntregaMonografiaOriginalForm(ModelForm):
    class Meta:
        model = EntregaMonografiaOriginal
        exclude = ('alunos', 'data','disciplina')
        
# class CobrarMonografiaimpressaForm(ModelForm):
#     class Meta:
#         model = CobrarMonografiaimpressa
#         exclude = ('data')
    
    
# class CobrarMonografiaatrasadaForm(ModelForm):
#      class Meta:
#         model = CobrarMonografiaatrasada
#         exclude = ('data')
#      def __init__(self, *args, **kwargs):
#         super( CobrarMonografiaatrasadaForm, self).__init__(*args, **kwargs)
#         self.fields['alunos'].widget = CheckboxSelectMultiple(choices=self.fields['alunos'].choices)

# class ReceberMonografiaForm(ModelForm):
#     class Meta:
#         model = ReceberMonografia
#         exclude = ('alunos','disciplina')
        
# class DevolucaoMonografiaIMpressaForm(ModelForm):
#     class Meta:
#         model = DevolucaoMonografiaIMpressa
#         exclude = ('alunos','disciplina')

