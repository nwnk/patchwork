# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import patchwork.models


class Migration(migrations.Migration):

    dependencies = [
        ('patchwork', '0002_load_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patch',
            name='state',
            field=models.ForeignKey(default=patchwork.models.get_default_initial_patch_state_pk, to='patchwork.State'),
        ),
    ]
