# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """ Create NewNotice instances for each Notice AND NoticeCFRPart """
        # We're going to create a new notice for every existing notice.
        for notice in orm.Notice.objects.all():
            # We need to create a new notice for each notice AND
            # cfr_part it applies to. 
            for cfr_part in notice.noticecfrpart_set.all():
                new_notice = orm.NewNotice(
                        document_number=notice.document_number,
                        cfr_part=cfr_part.cfr_part,
                        effective_on=notice.effective_on,
                        fr_url=notice.fr_url,
                        publication_date=notice.publication_date,
                        notice=notice.notice)
                new_notice.save()

    def backwards(self, orm):
        """ Create Notice AND NoticeCFRPart instances for each NewNotice """
        # For each NewNotice instance, we need to create a
        # NoticeCFRPart, and for each unique document number create a
        # Notice instance.
        for notice in orm.NewNotice.objects.all():
            # See if there is already a Notice with the document number,
            # if not, create it.
            existing_notices = Notice.objects.filter(
                document_number=notice.document_number)

            new_notice = existing_notices[0] \
                if len(existing_notices) == 0 \
                else orm.Notice(
                    document_number=notice.document_number,
                    effective_on=notice.effective_on,
                    fr_url=notice.fr_url,
                    publication_date=notice.publication_date,
                    notice=notice.notice)

            # Add the CFR part
            new_notice.noticecfrpart_set.create(cfr_part=notice.cfr_part)

            new_notice.save()

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
        u'regcore.notice': {
            'Meta': {'object_name': 'Notice'},
            'document_number': ('django.db.models.fields.SlugField', [], {'max_length': '20', 'primary_key': 'True'}),
            'effective_on': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fr_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notice': ('regcore.fields.CompressedJSONField', [], {}),
            'publication_date': ('django.db.models.fields.DateField', [], {})
        },
        u'regcore.noticecfrpart': {
            'Meta': {'unique_together': "(('notice', 'cfr_part'),)", 'object_name': 'NoticeCFRPart', 'index_together': "(('notice', 'cfr_part'),)"},
            'cfr_part': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['regcore.Notice']"})
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
    symmetrical = True
