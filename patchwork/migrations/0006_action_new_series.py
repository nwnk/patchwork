# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.core.management import call_command


def load_fixture(name):
    call_command('loaddata', name, app_label='patchwork', verbosity=0,
                 interactive=False)

def load_actions(apps, schema_editor):
    load_fixture('default_actions')

def reset_actions(apps, schema_editor):
    Action = apps.get_model('patchwork', 'Action')
    Action.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('patchwork', '0005_action_serieslog'),
    ]

    operations = [
        migrations.RunPython(load_actions, reset_actions),
    ]
