# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20160202_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='person',
            field=models.ForeignKey(to='app01.Person'),
            preserve_default=True,
        ),
    ]
