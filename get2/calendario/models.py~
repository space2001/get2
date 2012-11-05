from django.db import models
from django import forms
from django.contrib.auth.models import User,Group
import operator, datetime
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, AdminPasswordChangeForm

class Mansione(models.Model):
	descrizione = models.CharField('Descrizione',max_length=200)
	def __unicode__(self):
		return '%s' % (self.descrizione)
	# Milite tipo A, milite tipo B, centralinista ecc...

class MansioneForm(forms.ModelForm):
	class Meta:
		model = Mansione

class Persona(models.Model):
	user = models.ForeignKey(User, unique=True, blank=True, null=True, related_name='pers_user')
	nome = models.CharField('Nome',max_length=200)
	cognome = models.CharField('Cognome',max_length=200)
	nascita = models.DateField('Data di nascita')
	#caratteristiche della persona
	competenze = models.ManyToManyField(Mansione, blank=True, null=True)
	def notifiche_non_lette(self):
		n=0
		for m in Notifica.objects.filter(destinatario=self.user):
			if(m.letto == False):
				n+=1
		return n
	def __unicode__(self):
		return '%s %s' % (self.nome,self.cognome)

class PersonaForm(forms.ModelForm):
	#nascita = forms.DateField(label='Data di nascita', required=False, widget=widgets.AdminDateWidget)
	class Meta:
		model = Persona

class Gruppo(models.Model):
	nome = models.CharField('Nome',max_length=30)
	componenti = models.ManyToManyField(Persona, blank=True, null=True, related_name='componenti_gruppo')


class TipoTurno(models.Model):
	identificativo = models.CharField(max_length=30, blank=False)
	def __unicode__(self):
		return '%s' % (self.identificativo)

class TipoTurnoForm(forms.ModelForm):
	class Meta:
		model = TipoTurno


OPERATORI=(('=','Uguale a'),('>','Maggiore di'))

class Requisito(models.Model):
	mansione=models.ForeignKey(Mansione)
	operatore=models.CharField('operatore', max_length=10, choices=OPERATORI )
	valore=models.IntegerField()
	tipo_turno=models.ForeignKey(TipoTurno, related_name="req_tipo_turno")

class RequisitoForm(forms.ModelForm):
	class Meta:
		model = Requisito
		exclude = ('tipo_turno')

GIORNO = (
  (0, 'lunedi'),
  (1, 'martedi'),
  (2, 'mercoledi'),
  (3, 'giovedi'),
  (4, 'venerdi'),
  (5, 'sabato'),
  (6, 'domenica'),)

class Occorrenza(models.Model):
	pass


ops = {"=": operator.eq, ">": operator.gt}

class Turno(models.Model):
	identificativo = models.CharField(max_length=30, blank=True , default='')
	inizio = models.DateTimeField()
	fine = models.DateTimeField()
	tipo = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	occorrenza = models.ForeignKey(Occorrenza, blank=True, null=True)
	def coperto(self):
		if self.tipo:
			for r in Requisito.objects.filter(tipo_turno=self.tipo_id):
				contatore=0
				for d in self.turno_disponibilita.all():
					if (d.mansione==r.mansione):
						contatore+=1
						operatore=ops[r.operatore]
						if not operatore(contatore,r.valore):
							return False
		return True
	def contemporanei(self):
		i=self.inizio+datetime.timedelta(seconds=1)
		f=self.fine-datetime.timedelta(seconds=1)
		return Turno.objects.filter( (models.Q(inizio__lte=i) & models.Q(fine__gte=f)) | models.Q(inizio__range=(i ,f)) | models.Q(fine__range=(i,f)) ).exclude(id=self.id)

class TurnoForm(forms.ModelForm):
	class Meta:
		model = Turno
		exclude = ('occorrenza')

class TurnoFormRipeti(TurnoForm):
	inizio=forms.DateTimeField(widget=forms.SplitDateTimeWidget)
	fine=forms.DateTimeField(widget=forms.SplitDateTimeWidget)
	ripeti = forms.BooleanField(required=False)
	ripeti_da = forms.DateField(required=False)
	ripeti_al = forms.DateField(required=False)
	ripeti_il_giorno = forms.MultipleChoiceField(choices=GIORNO, widget=forms.CheckboxSelectMultiple(),required=False)
	def clean(self):
		data = self.cleaned_data
		ripeti=data.get('ripeti')
		da=data.get('ripeti_da')
		al=data.get('ripeti_al')
		if data.get('inizio')>data.get('fine'):
			raise forms.ValidationError('Il turno termina prima di iniziare! controlla inizio e fine')
		if ripeti and (da==None or al==None):
			raise forms.ValidationError('Specifica l\' intervallo in cui ripetere il turno')
		return data



DISPONIBILITA = (("Disponibile","Disponibile"),("Indisponibile","Indisponibile"),)

class Disponibilita(models.Model):
	tipo = models.CharField(max_length=20, choices=DISPONIBILITA)
	persona = models.ForeignKey(Persona, related_name='persona_disponibilita')
	ultima_modifica = models.DateTimeField()
	creata_da = models.ForeignKey(User, related_name='creata_da_disponibilita')
	turno = models.ForeignKey(Turno, related_name='turno_disponibilita')
	mansione = models.ForeignKey(Mansione)


class Notifica(models.Model):
	destinatario = models.ForeignKey(User, related_name='destinatario_user')
	data =  models.DateTimeField()
	testo = models.CharField(max_length=1000)
	letto = models.BooleanField()
	

class Log(models.Model):
	testo = models.CharField(max_length=50)
	data = models.DateTimeField()

class UserCreationForm2(UserCreationForm):
	email = forms.EmailField(label = "Email")
	class Meta:
		model = User
		fields = ("username", "email", )

class UserChangeForm2(UserChangeForm):
	class Meta:
		model = User
		fields = ("username", "email",)
	def clean_password(self):
		return "" # This is a temporary fix for a django 1.4 bug


