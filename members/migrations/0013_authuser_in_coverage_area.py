# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_auto_20150110_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='in_coverage_area',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
