# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patchwork', '0003_patch_state_default_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('submitted', models.DateTimeField(default=datetime.datetime.now)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('version', models.IntegerField(default=1)),
                ('n_patches', models.IntegerField(default=0)),
                ('project', models.ForeignKey(to='patchwork.Project')),
                ('reviewer', models.ForeignKey(related_name='reviewers', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('submitter', models.ForeignKey(related_name='submitters', to='patchwork.Person')),
            ],
        ),
        migrations.CreateModel(
            name='SeriesRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=1)),
                ('root_msgid', models.CharField(max_length=255)),
                ('cover_letter', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['version'],
            },
        ),
        migrations.CreateModel(
            name='SeriesRevisionPatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('patch', models.ForeignKey(to='patchwork.Patch')),
                ('revision', models.ForeignKey(to='patchwork.SeriesRevision')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='seriesrevision',
            name='patches',
            field=models.ManyToManyField(to='patchwork.Patch', through='patchwork.SeriesRevisionPatch'),
        ),
        migrations.AddField(
            model_name='seriesrevision',
            name='series',
            field=models.ForeignKey(to='patchwork.Series'),
        ),
        migrations.AlterUniqueTogether(
            name='seriesrevisionpatch',
            unique_together=set([('revision', 'patch')]),
        ),
        migrations.AlterUniqueTogether(
            name='seriesrevision',
            unique_together=set([('series', 'version')]),
        ),
    ]
