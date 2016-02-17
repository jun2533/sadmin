# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20160128_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Svname',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sname', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SvnVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(max_length=10)),
                ('sname', models.ForeignKey(to='app01.Svname')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
