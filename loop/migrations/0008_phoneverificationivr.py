# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0007_auto_20170214_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneVerificationIVR',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('call_id', models.CharField(max_length=100)),
                ('to_number', models.CharField(max_length=20)),
                ('responsed_digit', models.CharField(max_length=20, null=True, blank=True)),
                ('user_created', models.ForeignKey(related_name='loop_phoneverificationivr_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_phoneverificationivr_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
