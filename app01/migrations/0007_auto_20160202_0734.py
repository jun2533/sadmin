# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20160202_0607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='person',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AlterField(
            model_name='svnversion',
            name='version',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
