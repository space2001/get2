# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mansione'
        db.create_table('calendario_mansione', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descrizione', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('calendario', ['Mansione'])

        # Adding model 'Persona'
        db.create_table('calendario_persona', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pers_user', unique=True, null=True, to=orm['auth.User'])),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cognome', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nascita', self.gf('django.db.models.fields.DateField')()),
            ('stato', self.gf('django.db.models.fields.CharField')(default='disponibile', max_length=40)),
        ))
        db.send_create_signal('calendario', ['Persona'])

        # Adding M2M table for field competenze on 'Persona'
        db.create_table('calendario_persona_competenze', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('persona', models.ForeignKey(orm['calendario.persona'], null=False)),
            ('mansione', models.ForeignKey(orm['calendario.mansione'], null=False))
        ))
        db.create_unique('calendario_persona_competenze', ['persona_id', 'mansione_id'])

        # Adding model 'Gruppo'
        db.create_table('calendario_gruppo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('calendario', ['Gruppo'])

        # Adding M2M table for field componenti on 'Gruppo'
        db.create_table('calendario_gruppo_componenti', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gruppo', models.ForeignKey(orm['calendario.gruppo'], null=False)),
            ('persona', models.ForeignKey(orm['calendario.persona'], null=False))
        ))
        db.create_unique('calendario_gruppo_componenti', ['gruppo_id', 'persona_id'])

        # Adding model 'TipoTurno'
        db.create_table('calendario_tipoturno', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identificativo', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('calendario', ['TipoTurno'])

        # Adding model 'Requisito'
        db.create_table('calendario_requisito', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mansione', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['calendario.Mansione'])),
            ('operatore', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('valore', self.gf('django.db.models.fields.IntegerField')()),
            ('tipo_turno', self.gf('django.db.models.fields.related.ForeignKey')(related_name='req_tipo_turno', to=orm['calendario.TipoTurno'])),
        ))
        db.send_create_signal('calendario', ['Requisito'])

        # Adding model 'Occorrenza'
        db.create_table('calendario_occorrenza', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('calendario', ['Occorrenza'])

        # Adding model 'Turno'
        db.create_table('calendario_turno', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identificativo', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('inizio', self.gf('django.db.models.fields.DateTimeField')()),
            ('fine', self.gf('django.db.models.fields.DateTimeField')()),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['calendario.TipoTurno'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('occorrenza', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['calendario.Occorrenza'], null=True, blank=True)),
        ))
        db.send_create_signal('calendario', ['Turno'])

        # Adding model 'Disponibilita'
        db.create_table('calendario_disponibilita', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='persona_disponibilita', to=orm['calendario.Persona'])),
            ('ultima_modifica', self.gf('django.db.models.fields.DateTimeField')()),
            ('creata_da', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creata_da_disponibilita', to=orm['auth.User'])),
            ('turno', self.gf('django.db.models.fields.related.ForeignKey')(related_name='turno_disponibilita', to=orm['calendario.Turno'])),
            ('mansione', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['calendario.Mansione'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal('calendario', ['Disponibilita'])

        # Adding model 'Notifica'
        db.create_table('calendario_notifica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('destinatario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destinatario_user', to=orm['auth.User'])),
            ('data', self.gf('django.db.models.fields.DateTimeField')()),
            ('testo', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('letto', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('calendario', ['Notifica'])

        # Adding model 'Log'
        db.create_table('calendario_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('data', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('calendario', ['Log'])


    def backwards(self, orm):
        # Deleting model 'Mansione'
        db.delete_table('calendario_mansione')

        # Deleting model 'Persona'
        db.delete_table('calendario_persona')

        # Removing M2M table for field competenze on 'Persona'
        db.delete_table('calendario_persona_competenze')

        # Deleting model 'Gruppo'
        db.delete_table('calendario_gruppo')

        # Removing M2M table for field componenti on 'Gruppo'
        db.delete_table('calendario_gruppo_componenti')

        # Deleting model 'TipoTurno'
        db.delete_table('calendario_tipoturno')

        # Deleting model 'Requisito'
        db.delete_table('calendario_requisito')

        # Deleting model 'Occorrenza'
        db.delete_table('calendario_occorrenza')

        # Deleting model 'Turno'
        db.delete_table('calendario_turno')

        # Deleting model 'Disponibilita'
        db.delete_table('calendario_disponibilita')

        # Deleting model 'Notifica'
        db.delete_table('calendario_notifica')

        # Deleting model 'Log'
        db.delete_table('calendario_log')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'calendario.disponibilita': {
            'Meta': {'object_name': 'Disponibilita'},
            'creata_da': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creata_da_disponibilita'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mansione': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendario.Mansione']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'persona_disponibilita'", 'to': "orm['calendario.Persona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'turno': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'turno_disponibilita'", 'to': "orm['calendario.Turno']"}),
            'ultima_modifica': ('django.db.models.fields.DateTimeField', [], {})
        },
        'calendario.gruppo': {
            'Meta': {'object_name': 'Gruppo'},
            'componenti': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'componenti_gruppo'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['calendario.Persona']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'calendario.log': {
            'Meta': {'object_name': 'Log'},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'testo': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'calendario.mansione': {
            'Meta': {'object_name': 'Mansione'},
            'descrizione': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'calendario.notifica': {
            'Meta': {'object_name': 'Notifica'},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            'destinatario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destinatario_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'testo': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'calendario.occorrenza': {
            'Meta': {'object_name': 'Occorrenza'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'calendario.persona': {
            'Meta': {'object_name': 'Persona'},
            'cognome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'competenze': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['calendario.Mansione']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nascita': ('django.db.models.fields.DateField', [], {}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'stato': ('django.db.models.fields.CharField', [], {'default': "'disponibile'", 'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pers_user'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'calendario.requisito': {
            'Meta': {'object_name': 'Requisito'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mansione': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendario.Mansione']"}),
            'operatore': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tipo_turno': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'req_tipo_turno'", 'to': "orm['calendario.TipoTurno']"}),
            'valore': ('django.db.models.fields.IntegerField', [], {})
        },
        'calendario.tipoturno': {
            'Meta': {'object_name': 'TipoTurno'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificativo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'calendario.turno': {
            'Meta': {'object_name': 'Turno'},
            'fine': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificativo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'inizio': ('django.db.models.fields.DateTimeField', [], {}),
            'occorrenza': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendario.Occorrenza']", 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendario.TipoTurno']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['calendario']