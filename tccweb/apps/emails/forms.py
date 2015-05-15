from django.forms import ModelForm,  MultipleChoiceField, ValidationError, EmailField, CheckboxSelectMultiple
from emails.sendmail import options

class EnviaEmailForm(ModelForm):
    filtro = MultipleChoiceField(label='Filtro',required=False, widget=CheckboxSelectMultiple, choices=options())