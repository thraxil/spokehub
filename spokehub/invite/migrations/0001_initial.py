# flake8: noqa
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invite'
        db.create_table(u'invite_invite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.TextField')()),
            ('token', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.TextField')(default='OPEN')),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'invite', ['Invite'])


    def backwards(self, orm):
        # Deleting model 'Invite'
        db.delete_table(u'invite_invite')


    models = {
        u'invite.invite': {
            'Meta': {'object_name': 'Invite'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'default': "'OPEN'"}),
            'token': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['invite']
