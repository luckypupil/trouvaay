# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0029_product_colors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
    ]
