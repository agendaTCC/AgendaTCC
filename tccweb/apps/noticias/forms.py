from django.forms import ModelForm
from models import Noticia

class NoticiaForm(ModelForm):
    class Meta:
        model = Noticia
        exclude = ('autor')