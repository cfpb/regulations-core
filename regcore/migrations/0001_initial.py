# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import regcore.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.SlugField(max_length=200)),
                ('old_version', models.SlugField(max_length=20)),
                ('new_version', models.SlugField(max_length=20)),
                ('diff', regcore.fields.CompressedJSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.SlugField(max_length=20)),
                ('name', models.SlugField(max_length=20)),
                ('label', models.SlugField(max_length=200)),
                ('layer', regcore.fields.CompressedJSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_number', models.SlugField(max_length=20)),
                ('cfr_part', models.SlugField(max_length=200)),
                ('effective_on', models.DateField(null=True)),
                ('fr_url', models.CharField(max_length=200)),
                ('publication_date', models.DateField()),
                ('notice', regcore.fields.CompressedJSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Regulation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.SlugField(max_length=20)),
                ('label_string', models.SlugField(max_length=200)),
                ('text', models.TextField()),
                ('title', models.TextField(blank=True)),
                ('node_type', models.SlugField(max_length=10)),
                ('children', regcore.fields.CompressedJSONField()),
                ('root', models.BooleanField(default=False, db_index=True)),
                ('marker', models.CharField(default=b'', max_length=10)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='regulation',
            unique_together=set([('version', 'label_string')]),
        ),
        migrations.AlterIndexTogether(
            name='regulation',
            index_together=set([('version', 'label_string')]),
        ),
        migrations.AlterUniqueTogether(
            name='notice',
            unique_together=set([('document_number', 'cfr_part')]),
        ),
        migrations.AlterIndexTogether(
            name='notice',
            index_together=set([('document_number', 'cfr_part')]),
        ),
        migrations.AlterUniqueTogether(
            name='layer',
            unique_together=set([('version', 'name', 'label')]),
        ),
        migrations.AlterIndexTogether(
            name='layer',
            index_together=set([('version', 'name', 'label')]),
        ),
        migrations.AlterUniqueTogether(
            name='diff',
            unique_together=set([('label', 'old_version', 'new_version')]),
        ),
        migrations.AlterIndexTogether(
            name='diff',
            index_together=set([('label', 'old_version', 'new_version')]),
        ),
    ]
