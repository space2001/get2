#template_filters.py
import pdb
from django import template
register = template.Library()
from get2.calendario.views import *
from django.forms.models import model_to_dict

@register.filter
def verifica_requisito(instance, arg):
	#pdb.set_trace()
	return instance.verifica_requisito(arg)
# template usage
#{{ instance|verifica_requisito:"value1" }}

@register.filter
def gia_disponibile(instance, arg):
	if instance.persona_disponibilita.filter(turno=arg,tipo="Disponibile"):
		return instance.persona_disponibilita.filter(turno=arg,tipo="Disponibile")[0].id
	return False

@register.filter
def occorrenze(instance, arg):
	return Turno.objects.filter(occorrenza=arg)

@register.filter
def turno_futuro(instance):
	return instance.inizio>datetime.datetime.now()

@register.filter
def turno_intervallo_disponibilita(instance):
	return verifica_intervallo(instance)[0]
	
@register.filter
def errore_turno_intervallo_disponibilita(instance):
	return verifica_intervallo(instance)[1]
	
@register.filter
def stampa_requisito(instance):
	s=""
	r_as_dict = model_to_dict(instance)
	f=RequisitoForm(r_as_dict)
	if f.is_valid():
		for campo in f.fields.keys():
			val=str(f.cleaned_data[campo])
			if val=="True":
				val="<div class='si'></div>"
			elif val=="False":
				val="<div class='no'></div>"
			s+="<td>"+val+"</td>"
		s+='<td class="operazioni superuser"><a href="/impostazioni/requisito/modifica/'+str(instance.id)+'/"><span class="img_modifica"></span></a><a href="/impostazioni/requisito/elimina/'+str(instance.id)+'/"><span class="img_elimina"></span></a></td>'
	return s
stampa_requisito.is_safe = True
