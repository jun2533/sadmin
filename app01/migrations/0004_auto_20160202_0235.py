# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_svname_svnversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='svname',
            name='sname',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
