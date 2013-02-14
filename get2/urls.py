from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += patterns('get2.calendario',
	# calendario
	(r'^calendario/$', 'views.calendario'),
	(r'^calendario/(?P<azione>\w+)$', 'views.calendarioazione'),
	# persone
	(r'^persone/$', 'views.elenco_persona'),
	(r'^persone/nuovo/$', 'views.nuovo_persona'),
	(r'^persone/modifica/(?P<persona_id>\w+)/$', 'views.modifica_persona'),
	# utenti
	(r'^utenti/$', 'views.elenco_utente'),
	(r'^utenti/nuovo/$', 'views.nuovo_utente'),
	(r'^utenti/modifica/(?P<utente_id>\w+)/password/$', 'views.modifica_password_utente'),
	(r'^utenti/modifica/(?P<utente_id>\w+)/$', 'views.modifica_utente'),
	# mansioni
	(r'^impostazioni/mansione/nuovo/$', 'views.nuovo_mansione'),
	(r'^impostazioni/mansione/modifica/(?P<mansione_id>\w+)/$', 'views.modifica_mansione'),
	(r'^impostazioni/mansione/elimina/(?P<mansione_id>\w+)/$', 'views.elimina_mansione'),
	# turno
	(r'^calendario/turno/nuovo/$', 'views.nuovo_turno'),
	(r'^calendario/turno/modifica/(?P<turno_id>\w+)/$', 'views.modifica_turno'),
	(r'^calendario/turno/elimina/(?P<turno_id>\w+)/$', 'views.elimina_turno'),
	(r'^calendario/cerca_persona/(?P<turno_id>\w+)/(?P<mansione_id>\w+)', 'views.cerca_persona'),
	(r'^calendario/disponibilita/(?P<turno_id>\w+)/(?P<mansione_id>\w+)/(?P<persona_id>\w+)/(?P<disponibilita>\w+)', 'views.disponibilita_url'),
	(r'^calendario/rimuovi_disponibilita/(?P<disp_id>\w+)', 'views.rimuovi_disponibilita'),
	#(r'^turno/cerca_persona/(?P<turno_id>\w+)/(?P<mansione_id>\w+)/$', 'views.turno_cerca'),
	# impostazioni
	(r'^impostazioni/$', 'views.impostazioni'),
	(r'^impostazioni/tipo_turno/nuovo/$', 'views.nuovo_tipo_turno'),
	(r'^impostazioni/tipo_turno/modifica/(?P<tipo_turno_id>\w+)/$', 'views.modifica_tipo_turno'),
	(r'^impostazioni/tipo_turno/elimina/(?P<tipo_turno_id>\w+)/$', 'views.elimina_tipo_turno'),
)

urlpatterns += patterns('django.contrib.auth.views',
    #utente
    #(r'^utente/nuovo/$', 'turni.views.nuovoutente'),
    (r'^utenti/modifica_password/$', 'password_change'),
    (r'^utenti/modifica_password/ok/$', 'password_change_done'),
    (r'^utenti/reset/$', 'password_reset'),
    (r'^utenti/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'^utenti/reset/completa/$', 'password_reset_complete'),
    (r'^utenti/reset/ok/$', 'password_reset_done'),
    )

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'} ),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/calendario/'}),
    )

#Notifiche
urlpatterns += patterns('nano.privmsg.views',
url(r'^notifiche/add$',          'add_pm', name='add_pm'),
url(r'^notifiche/(?P<msgid>[1-9][0-9]*)/archive$', 'move_to_archive', name='archive_pm'),
url(r'^notifiche/(?P<msgid>[1-9][0-9]*)/delete$', 'delete', name='delete_pm'),
#url(r'^(?:(?P<action>(archive|sent))/?)?$', 'show_pms', name='show_pms'),
url(r'^notifiche/archive/$', 'show_pm_archived', name='show_archived_pms'),
url(r'^notifiche/sent/$', 'show_pm_sent', name='show_sent_pms'),
url(r'^notifiche/$', 'show_pm_received', name='show_pms'),
#url(r'^$', 'show_pms', {u'action': u'received'}, name='show_pms'),
)

