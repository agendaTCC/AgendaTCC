from django.conf import settings
# from departamentos.models import Departamento


def django_conf(request):
    grupos = None
    # grupos = Departamento.objects.all()
    return {'settings': settings, 'grupos_iniciais':grupos,}
