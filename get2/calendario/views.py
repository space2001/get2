# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from get2.calendario.models import *
from django.shortcuts import render_to_response
import calendar,datetime,locale
from django.db.models import Q, Count
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm 
from django.contrib.auth.decorators import login_required
import pdb
from django.template import RequestContext
from django.forms.formsets import formset_factory
import settings_calendario

####   persona   ####


def elenco_persona(request):
	#if request.user.is_staff:
	persone = Persona.objects.all().order_by('cognome')
	gruppi = Gruppo.objects.all()
	mansioni = Mansione.objects.all()
	risposta = HttpResponse(render_to_response('elenco_persona.html',{'persone':persone,'stati':STATI,'request':request,'gruppi':gruppi,'mansioni':mansioni}))
	return risposta
	#else:
	#	return render_to_response('staff-no.html')


def nuovo_persona(request):
	#if request.user.is_staff:
	azione = 'nuovo'
	if request.method == 'POST':
		form = PersonaForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone')
	else:
		form = PersonaForm()
	return render_to_response('form_persona.html',{'request':request,'form': form,'azione': azione,'mansione_form':MansioneForm()}, RequestContext(request))
	#else:
	#	return render_to_response('staff-no.html')

def modifica_persona(request,persona_id):
	azione = 'modifica'
	per = Persona.objects.get(id=persona_id)
	if request.method == 'POST':  # If the form has been submitted...
		form = PersonaForm(request.POST, instance=per)  # necessario per modificare la riga preesistente
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/persone/elenco') # Redirect after POST
	else:
		form = PersonaForm(instance=per)
	return render_to_response('form_persona.html',{'request': request, 'form': form,'azione': azione, 'per': per,'mansione_form':MansioneForm()}, RequestContext(request))

####   fine persona   ####

#####   calendario   ####

def calendario(request):
	if request.COOKIES.has_key('anno'):
		anno=int(request.COOKIES['anno'])
	else:
		anno=datetime.datetime.today().year

	if request.COOKIES.has_key('mese'):
		mese=int(request.COOKIES['mese'])
	else:
		mese=datetime.datetime.today().month

	if request.COOKIES.has_key('giorno'):
		giorno=int(request.COOKIES['giorno'])
	else:
		giorno=datetime.datetime.today().day

	start=datetime.datetime(anno,mese,giorno,1)
	giorni = []
	turni = []
	for i in range(0,7):
		giorni.append(start)
		stop = start + datetime.timedelta(days=1)
		turni.append(Turno.objects.filter(inizio__range=(start, stop)).order_by('inizio'))
		start = start + datetime.timedelta(days=1)
	start = datetime.datetime(anno,mese,giorno,1)
	
	calendario = []
	calendario.append(giorni)
	calendario.append(turni)
	calendario=zip(*calendario)
	tipo_turno=TipoTurno.objects.all()
	corpo=render_to_response('calendario.html',{'calendario':calendario,'start':start,'request':request,'tipo_turno':tipo_turno}, RequestContext(request))
	risposta = HttpResponse(corpo)
	risposta.set_cookie('anno', value=anno)
	risposta.set_cookie('mese', value=mese)
	risposta.set_cookie('giorno', value=giorno)
	risposta.set_cookie('sezione', value='calendario')
	return risposta

def calendarioazione(request,azione):
	start = datetime.datetime(int(request.COOKIES['anno']),int(request.COOKIES['mese']),int(request.COOKIES['giorno']))
	if azione == 'oggi':
		start = datetime.datetime.today()
	if azione == 'avanti':
		start += datetime.timedelta(days=1)
	if azione == 'indietro':
		start -= datetime.timedelta(days=1)
	if azione == 'settavanti':
		start += datetime.timedelta(days=7)
	if azione == 'settindietro':
		start -= datetime.timedelta(days=7)
	risposta = HttpResponseRedirect('/calendario/')
	risposta.set_cookie('anno', value=start.year)
	risposta.set_cookie('mese', value=start.month)
	risposta.set_cookie('giorno', value=start.day)
	return risposta

def cerca_persona(request, turno_id, mansione_id):
	mansione=Mansione.objects.get(id=mansione_id)
	persone=Persona.objects.filter(competenze=mansione)
	turno=Turno.objects.get(id=turno_id)
	return render_to_response('cerca_persona.html',{'persone':persone,'turno':turno,'mansione':mansione,'DISPONIBILITA':DISPONIBILITA,'request':request})


####   fine calendario   ####

####   disponibilita   ####

DISP_MIN=1
DISP_MAX=20

def disponibilita_verifica_tempo(request, turno):
#	pdb.set_trace()
	if request.user.is_staff:
		verifica=True
		errore=''
	else:
		now=datetime.datetime.now()
		diff=turno.inizio-now
		if diff.days<0:
			verifica=False
			errore='passato'
		elif diff.days<DISP_MIN:
			verifica=False
			errore='vicino'
		elif diff.days>DISP_MAX:
			verifica=False
			errore='lontano'
		else:
			verifica=True
			errore=''
	#cprint errore
	#print diff.days
	return (verifica,errore)


def rimuovi_disponibilita(request, disp_id):
	d=Disponibilita.objects.get(id=disp_id)
	d.tipo='Indisponibile'
	d.save()
	return HttpResponseRedirect('/calendario')

def disponibilita_risolvi_contemporaneo(request,persona_id,contemporaneo):
	if Disponibilita.objects.filter(persona_id=persona_id,turno=contemporaneo).exists():
		for d in Disponibilita.objects.filter(persona_id=persona_id,turno=contemporaneo):
			#if d.tipo=="Disponibile":
				#persona= Persona.objects.get(id=persona_id)
				#notifica_disponibilita(request,persona,contemporaneo,'Non piu disponibile',contemporaneo.mansione)
			rimuovi_disponibilita(d.id)


def nuova_disponibilita(request, turno_id, mansione_id, persona_id, disponibilita):
	#inizializzo ma non salvo un oggetto disponibilita
	#pdb.set_trace()
	disp=Disponibilita()
	disp.tipo=disponibilita
	disp.persona=Persona.objects.get(id=persona_id)
	disp.ultima_modifica=datetime.datetime.now()
	disp.creata_da=request.user
	disp.turno=Turno.objects.get(id=turno_id)
	disp.mansione=Mansione.objects.get(id=mansione_id)
	#verifico se la disponibilita e entro i tempi corretti
	verifica_tempo=disponibilita_verifica_tempo(request, disp.turno)
	if verifica_tempo[0]:
		#una persona puo avere una sola disponibilita per turno
		if Disponibilita.objects.filter(persona=disp.persona,turno=disp.turno ).exists():
			esistente=Disponibilita.objects.get(persona=disp.persona, turno=disp.turno )
			#if esistente.tipo=='Disponibile':
				#notifica_disponibilita(request,esistente.persona,esistente.turno,'Non piu disponibile',esistente.mansione)
			esistente.delete()
		#risolvo i conflitti con i turni contemporanei
		for contemporaneo in disp.turno.contemporanei():
			disponibilita_risolvi_contemporaneo(request,persona_id,contemporaneo)
		disp.save()
		#if not request.user.is_staff:
			#notifica_disponibilita(request,disponibilita.persona,disponibilita.turno,tipo_disponibilita,disponibilita.mansione)
	return verifica_tempo


def disponibilita_url(request, turno_id, mansione_id, persona_id, disponibilita):
	d=nuova_disponibilita(request, turno_id, mansione_id, persona_id, disponibilita)
	if d[0]:
		return HttpResponseRedirect('/calendario')
	else:
		print d[1]

####   fine disponibilita   ####

####   notifica   ####

def notifica_disponibilita(request,persona,turno,tipo_disponibilita,mansione):
	for n in NOTIFICHE:
		if turno.inizio.weekday() in n['giorni']:
			messaggio=str(persona) + ' si e reso <b>' + str(tipo_disponibilita) + '</b> con mansione di <b>'+ str(mansione) +'</b> per il turno <b>' + 'turno' + '</b>'
			now=datetime.datetime.now()
			notifica=Notifica()
			notifica.testo=messaggio
			notifica.data=now
			notifica.letto=False
			destinatario_id=n['id_utente']
			notifica.destinatario_id=destinatario_id
			notifica.save()
	return True

def elenco_notifica(request):
	u=request.user
	notifiche=Notifica.objects.filter(destinatario=u).order_by('data').reverse()
	return render_to_response('notifiche.html',{'notifiche':notifiche,'request':request})

####   fine notifica   ####

####   inizio utenti   ####

def elenco_utente(request):
	#if request.user.is_staff:
	utenti = User.objects.all()
	persone = Persona.objects.all()
	risposta = HttpResponse(render_to_response('elenco_utente.html',{'utenti':utenti,'persone':persone,'request':request,}))
	return risposta
	#else:
	#	return render_to_response('staff-no.html')

def nuovo_utente(request):
	#if request.user.is_staff:
	# Do something for anonymous users.
	azione = 'nuovo';
	if request.method == 'POST': # If the form has been submitted...
		form = UserCreationForm2(request.POST) # A form bound to the POST data
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/utenti/') # Redirect after POST
	else:
		form = UserCreationForm2()
	return render_to_response('form_utente.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))

def modifica_utente(request,utente_id):
	azione = 'modifica'
	user = User.objects.get(id=utente_id)
	if request.method == 'POST': # If the form has been submitted..
		form = UserChangeForm2(request.POST, instance=user,)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/utenti/') # Redirect after POST
	else:
		form = UserChangeForm2(instance=user)
	return render_to_response('form_utente.html',{'request':request, 'form': form,'azione': azione, 'user': user,}, RequestContext(request))

def modifica_password_utente(request,utente_id):
	user = User.objects.get(id=utente_id)
	if request.method == 'POST': # If the form has been submitted...
		form = AdminPasswordChangeForm(user=user, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/utenti/') # Redirect after POST
	else:
		form = AdminPasswordChangeForm(user=user)
	return render_to_response('form_password_utente.html',{'request':request, 'form': form, 'user': user,}, RequestContext(request))
	
####   fine utenti   ####

#### inizio mansioni ####

def nuovo_mansione(request):
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		form = MansioneForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni') # Redirect after POST
	else:
		form = MansioneForm()
	return render_to_response('form_mansione.html',{'request':request, 'form': form,'azione': azione}, RequestContext(request))	

def modifica_mansione(request, mansione_id):
	azione = 'modifica'
	mansione = Mansione.objects.get(id=mansione_id)
	if request.method == 'POST': # If the form has been submitted...
		form = MansioneForm(request.POST, instance=mansione) # necessario per modificare la riga preesistente
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		form = MansioneForm(instance=mansione)
	return render_to_response('form_mansione.html',{'form':form,'azione': azione, 'mansione': mansione,'request':request}, RequestContext(request))

def elimina_mansione(request,mansione_id):
	m=TipoTurno.objects.get(id=mansione_id)
	m.delete()
	return HttpResponseRedirect('/impostazioni/')

#### fine mansioni ####

#### inzio tipo turno ####

def impostazioni(request):
	tipi_turno=TipoTurno.objects.all()
	return render_to_response('impostazioni.html',{'tipi_turno':tipi_turno,'tipo_turno_form':TipoTurnoForm(),'operatori':OPERATORI,'mansioni':Mansione.objects.all(),'request':request}, RequestContext(request))


def nuovo_tipo_turno(request):
	azione = 'nuovo'
	if request.method == 'POST': # If the form has been submitted...
		tipo_turno_form = TipoTurnoForm(request.POST) # A form bound to the POST data
		if tipo_turno_form.is_valid():
			tipo_turno_form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		tipo_turno_form = TipoTurnoForm()
	return render_to_response('form_tipo_turno.html',{'tipo_turno_form':tipo_turno_form,'azione':azione,'request':request}, RequestContext(request))

def modifica_tipo_turno(request, tipo_turno_id):
	azione = 'modifica';
	tipo_turno = TipoTurno.objects.get(id=tipo_turno_id)
	if request.method == 'POST': # If the form has been submitted...
		tipo_turno_form = TipoTurnoForm(request.POST, instance=tipo_turno) # necessario per modificare la riga preesistente
		if tipo_turno_form.is_valid():
			tipo_turno_form.save()
			return HttpResponseRedirect('/impostazioni/') # Redirect after POST
	else:
		tipo_turno_form = TipoTurnoForm(instance=tipo_turno)
	return render_to_response('form_tipo_turno.html',{'tipo_turno_form': tipo_turno_form,'azione': azione, 'tipo_turno': tipo_turno,'request':request}, RequestContext(request))

def elimina_tipo_turno(request,tipo_turno_id):
	t=TipoTurno.objects.get(id=tipo_turno_id)
	t.delete()
	return HttpResponseRedirect('/impostazioni/')


#### fine tipo turno ####

#### inizio turno ####

def nuovo_turno(request):
	azione = 'Aggiungi'
	if request.method == 'POST': # If the form has been submitted...
		form = TurnoFormRipeti(request.POST) # A form bound to the POST data
		if form.is_valid():
			data = form.cleaned_data
			form.save()
			if data.get('ripeti'):
				o=Occorrenza()
				o.save()
				start=data.get('ripeti_da')
				stop=data.get('ripeti_al')
				giorno=data.get('ripeti_il_giorno')
				ora_inizio=data.get('inizio').time()
				start=datetime.datetime.combine(start,ora_inizio)
				durata=data.get('fine')-data.get('inizio')
				delta = datetime.timedelta(days=1)
				data['tipo']=data['tipo'].id
				data['occorrenza']=o.id
				#pdb.set_trace()
				while (start.date()<=stop):
					data['inizio_0']=start.date()
					data['fine_0']=(start+durata).date()
					data['inizio_1']=start.time()
					data['fine_1']=(start+durata).time()
					f=TurnoFormRipeti(data)
					if str(start.weekday()) in giorno and f.is_valid():
						t=f.save()
						t.occorrenza=o
						t.save()
					start+=delta
				
			return HttpResponseRedirect('/calendario/') # Redirect after POST
	else:
		form = TurnoFormRipeti()
	return render_to_response('form_turno.html',{'form': form,'azione': azione,'request':request}, RequestContext(request))

def modifica_turno(request, turno_id):
	azione = 'Modifica';
	turno = Turno.objects.get(id=turno_id)
	if request.method == 'POST': # If the form has been submitted...
		form = TurnoForm(request.POST, instance=turno) # necessario per modificare la riga preesistente
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/calendario/') # Redirect after POST
	else:
		form = TurnoForm(instance=turno)
	return render_to_response('form_turno.html',{'form': form,'azione': azione, 'turno_id': turno_id,'request':request}, RequestContext(request))

def elimina_turno(request, turno_id):
	t = Turno.objects.get(id=turno_id)
	t.delete()
	return HttpResponseRedirect('/calendario/')

def elimina_turno_occorrenza_succ(request, occorrenza_id):
	o=Occorrenza.objects.get(id=occorrenza_id)
	turni = Turno.objects.filter(occorrenza=o, inizio__gte=datetime.datetime.now())
	for t in turni:
		t.delete()
	return HttpResponseRedirect('/calendario/')

def elimina_turno_occorrenza(request, occorrenza_id):
	o=Occorrenza.objects.get(id=occorrenza_id)
	turni = Turno.objects.filter(occorrenza=o)
	for t in turni:
		t.delete()
	return HttpResponseRedirect('/calendario/')

#### fine turno ####


#### inizio statistiche ####
elenco_statistiche=("Turni totali",
			)

def statistiche(request):
	#se l' intervallo non e specificato prendo tutto
	dati=statistiche_intervallo(request,datetime.date(2000,1,1),datetime.datetime.now().date())
	return render_to_response('statistiche.html',{'dati': dati,'elenco_statistiche':elenco_statistiche,'request':request}, RequestContext(request))

def statistiche_intervallo(request, inizio, fine):
	#la funzione calcola le statistiche tra due date, rihiede 2 oggetti datetime.date
	dati=[]
	dati.append(elenco_statistiche)
	stat=[]
	stat.append(Persona.objects.filter(persona_disponibilita__tipo="Disponibile", persona_disponibilita__turno__inizio__gte=inizio, persona_disponibilita__turno__fine__lte=fine ).annotate(tot_turni=Count('persona_disponibilita')))
	#pdb.set_trace()
	dati.append(stat)
	dati=zip(*dati)
	#risp=Persona.objects.filter(persona_disponibilita__tipo="Disponibile").annotate(tot_turni=Count('persona_disponibilita'))
	return dati


#### fine statistiche ####
