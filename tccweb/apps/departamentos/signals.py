# from django.db.models.signals import post_save, m2m_changed
# from django.contrib.auth.models import Group
# from django.db.models import Q 
# from disciplinas.models import Disciplina
# from models import Monitor

# def transformar_monitor(sender,**kwargs):
#     monitor_do_grupo = kwargs['instance']
#     monitor = monitor_do_grupo.monitor.get_profile()
#     disciplinas_ = monitor_do_grupo.grupo.disciplinas.all()
#     busca = Q()
#     for disciplina in disciplinas_:
#         busca.add(Q(titulo = disciplina.id) & Q(semestre = monitor_do_grupo.semestre) & Q(ano = monitor_do_grupo.ano), busca.OR)
#     disciplinas = Disciplina.objects.filter(busca)
    
#     if int(monitor.funcao) == 4:
#         default_group = Group.objects.get(id = 6)
#         print default_group 
#     elif int(monitor.funcao) == 2 or int(monitor.funcao) == 3:
#         default_group = Group.objects.get(id = 7)
#     else:
#         default_group = Group.objects.get(id = int(monitor.funcao))
#     default_group.user_set.add(monitor.id) 
#     default_group.save()
   
#     for disciplina in disciplinas:
#         if monitor not in disciplina.monitores.all():
#             disciplina.monitores.add(monitor)
            
# post_save.connect(transformar_monitor, sender=Monitor, dispatch_uid="bancas.models.Monitor")
            
#     