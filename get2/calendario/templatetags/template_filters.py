#template_filters.py
import pdb
from django import template
register = template.Library()
from get2.calendario.views import *

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
