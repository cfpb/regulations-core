# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'NewNotice', fields ['document_number', 'cfr_part']
        db.delete_unique(u'regcore_newnotice', ['document_number', 'cfr_part'])

        # Removing index on 'NewNotice', fields ['document_number', 'cfr_part']
        db.delete_index(u'regcore_newnotice', ['document_number', 'cfr_part'])

        # Rename the table
        db.rename_table(u'regcore_newnotice', u'regcore_notice')

        # Adding unique constraint on 'Notice', fields ['document_number', 'cfr_part']
        db.create_unique(u'regcore_notice', ['document_number', 'cfr_part'])

        # Adding index on 'Notice', fields ['document_number', 'cfr_part']
        db.create_index(u'regcore_notice', ['document_number', 'cfr_part'])


    def backwards(self, orm):
        # Removing index on 'Notice', fields ['document_number', 'cfr_part']
        db.delete_index(u'regcore_notice', ['document_number', 'cfr_part'])

        # Removing unique constraint on 'Notice', fields ['document_number', 'cfr_part']
        db.delete_unique(u'regcore_notice', ['document_number', 'cfr_part'])

        # Rename the table
        db.rename_table(u'regcore_notice', u'regcore_newnotice')

        # Adding index on 'NewNotice', fields ['document_number', 'cfr_part']
        db.create_index(u'regcore_newnotice', ['document_number', 'cfr_part'])

        # Adding unique constraint on 'NewNotice', fields ['document_number', 'cfr_part']
        db.create_unique(u'regcore_newnotice', ['document_number', 'cfr_part'])


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
        u'regcore.notice': {
            'Meta': {'unique_together': "(('document_number', 'cfr_part'),)", 'object_name': 'Notice', 'index_together': "(('document_number', 'cfr_part'),)"},
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
