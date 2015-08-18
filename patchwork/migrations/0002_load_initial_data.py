# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command


# https://docs.djangoproject.com/en/1.8/topics/migrations/#data-migrations

def load_fixture(name):
    call_command('loaddata', name, app_label='patchwork', verbosity=0,
                 interactive=False)

def load_states(apps, schema_editor):
    load_fixture('default_states')

def load_tags(apps, schema_editor):
    load_fixture('default_tags')

def reset_states(apps, schema_editor):
    State = apps.get_model('patchwork', 'State')
    State.objects.all().delete()

def reset_tags(apps, schema_editor):
    Tag = apps.get_model('patchwork', 'Tag')
    Tag.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('patchwork', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_states, reset_states),
        migrations.RunPython(load_tags, reset_tags),
    ]
