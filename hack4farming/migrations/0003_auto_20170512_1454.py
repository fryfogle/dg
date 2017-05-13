# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hack4farming', '0002_auto_20170512_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='requirementclass',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='buyrent',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='requesttype',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='requirementclass',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='unit',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='suppliercategory',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
    ]
