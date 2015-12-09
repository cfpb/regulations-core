# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'NoticeCFRPart', fields ['notice', 'cfr_part']
        db.delete_unique(u'regcore_noticecfrpart', ['notice_id', 'cfr_part'])

        # Removing index on 'NoticeCFRPart', fields ['notice', 'cfr_part']
        db.delete_index(u'regcore_noticecfrpart', ['notice_id', 'cfr_part'])

        # Deleting model 'Notice'
        db.delete_table(u'regcore_notice')

        # Deleting model 'NoticeCFRPart'
        db.delete_table(u'regcore_noticecfrpart')


    def backwards(self, orm):
        # Adding index on 'NoticeCFRPart', fields ['notice', 'cfr_part']
        db.create_index(u'regcore_noticecfrpart', ['notice_id', 'cfr_part'])

        # Adding model 'Notice'
        db.create_table(u'regcore_notice', (
            ('notice', self.gf('regcore.fields.CompressedJSONField')()),
            ('effective_on', self.gf('django.db.models.fields.DateField')(null=True)),
            ('document_number', self.gf('django.db.models.fields.SlugField')(max_length=20, primary_key=True)),
            ('fr_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('publication_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'regcore', ['Notice'])

        # Adding model 'NoticeCFRPart'
        db.create_table(u'regcore_noticecfrpart', (
            ('notice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regcore.Notice'])),
            ('cfr_part', self.gf('django.db.models.fields.SlugField')(max_length=10)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'regcore', ['NoticeCFRPart'])

        # Adding unique constraint on 'NoticeCFRPart', fields ['notice', 'cfr_part']
        db.create_unique(u'regcore_noticecfrpart', ['notice_id', 'cfr_part'])


    models = {
        u'regcore.diff': {
            'Meta': {'unique_together': "(('label', 'old_version', 'new_version'),)", 'object_name': 'Diff', 'index_together': "(('label', 'old_version', 'new_version'),)"},
            'diff': ('regcore.fields.CompressedJSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'new_version': ('django.db.models.fields.SlugField', [], {'max_length': '20'}),
            'old_version': ('django.db.models.fields.SlugField', [], {'max_length': '20'})
        },
        u'regcore.layer': {
            'Meta': {'unique_together': "(('version', 'name', 'label'),)", 'object_name': 'Layer', 'index_together': "(('version', 'name', 'label'),)"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'layer': ('regcore.fields.CompressedJSONField', [], {}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '20'}),
            'version': ('django.db.models.fields.SlugField', [], {'max_length': '20'})
        },
        u'regcore.newnotice': {
            'Meta': {'unique_together': "(('document_number', 'cfr_part'),)", 'object_name': 'NewNotice', 'index_together': "(('document_number', 'cfr_part'),)"},
            'cfr_part': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'document_number': ('django.db.models.fields.SlugField', [], {'max_length': '20'}),
            'effective_on': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fr_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notice': ('regcore.fields.CompressedJSONField', [], {}),
            'publication_date': ('django.db.models.fields.DateField', [], {})
        },
        u'regcore.regulation': {
            'Meta': {'unique_together': "(('version', 'label_string'),)", 'object_name': 'Regulation', 'index_together': "(('version', 'label_string'),)"},
            'children': ('regcore.fields.CompressedJSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_string': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'marker': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'node_type': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'root': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.SlugField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['regcore']
