from django.conf.urls import patterns, url, include


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
	# persona
	(r'^persona/nuovo/$', 'views.nuovo_persona'),
	(r'^persona/elenco/$', 'views.elenco_persona'),
	(r'^persona/modifica/(?P<persona_id>\w+)/$', 'views.modifica_persona'),
	# utente
	(r'^utente/nuovo/$', 'views.nuovo_utente'),
	(r'^utente/elenco/$', 'views.elenco_utente'),
	(r'^utente/modifica/(?P<utente_id>\w+)/password/$', 'views.modifica_password_utente'),
	(r'^utente/modifica/(?P<utente_id>\w+)/$', 'views.modifica_utente'),
	# notifica
	(r'^notifica/elenco/$', 'views.elenco_notifica'),
	# tipo turno
	(r'^tipo_turno/elenco/$', 'views.elenco_tipo_turno'),
	# turno
	(r'^turno/nuovo/$', 'views.nuovo_turno'),
	(r'^turno/modifica/(?P<turno_id>\w+)/$', 'views.modifica_turno'),
	(r'^turno/elimina/(?P<turno_id>\w+)/$', 'views.elimina_turno'),
	# occorrenza
)

urlpatterns += patterns('django.contrib.auth.views',
    #utente
    #(r'^utente/nuovo/$', 'turni.views.nuovoutente'),
    (r'^utente/modifica_password/$', 'password_change'),
    (r'^utente/modifica_password/ok/$', 'password_change_done'),
    (r'^utente/reset/$', 'password_reset'),
    (r'^utente/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
    (r'^utente/reset/completa/$', 'password_reset_complete'),
    (r'^utente/reset/ok/$', 'password_reset_done'),
    )

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', ),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/calendario/'}),
    )
