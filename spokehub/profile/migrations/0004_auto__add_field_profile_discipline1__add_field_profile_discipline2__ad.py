# flake8: noqa
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.discipline1'
        db.add_column(u'profile_profile', 'discipline1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)

        # Adding field 'Profile.discipline2'
        db.add_column(u'profile_profile', 'discipline2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)

        # Adding field 'Profile.discipline3'
        db.add_column(u'profile_profile', 'discipline3',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)

        # Adding field 'Profile.website_url'
        db.add_column(u'profile_profile', 'website_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)

        # Adding field 'Profile.website_name'
        db.add_column(u'profile_profile', 'website_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.discipline1'
        db.delete_column(u'profile_profile', 'discipline1')

        # Deleting field 'Profile.discipline2'
        db.delete_column(u'profile_profile', 'discipline2')

        # Deleting field 'Profile.discipline3'
        db.delete_column(u'profile_profile', 'discipline3')

        # Deleting field 'Profile.website_url'
        db.delete_column(u'profile_profile', 'website_url')

        # Deleting field 'Profile.website_name'
        db.delete_column(u'profile_profile', 'website_name')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'profile.profile': {
            'Meta': {'object_name': 'Profile'},
            'about_me': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'discipline1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'discipline2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'discipline3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'website_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'website_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'})
        }
    }

    complete_apps = ['profile']
