# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0024_auto_20180116_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerQRScan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('timestamp', models.DateTimeField(null=True, blank=True)),
                ('qr_code', models.IntegerField(default=None)),
                ('action', models.IntegerField(default=0, choices=[(1, b'Pick Up'), (2, b'Payment')])),
                ('user_created', models.ForeignKey(related_name='loop_farmerqrscan_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_farmerqrscan_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FarmerTransportCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('code', models.IntegerField(null=True, blank=True)),
                ('phone', models.IntegerField(null=True, blank=True)),
                ('dateUsed', models.DateField(null=True, blank=True)),
                ('user_created', models.ForeignKey(related_name='loop_farmertransportcode_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='loop_farmertransportcode_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegistrationSms',
            fields=[
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('sms_status', models.IntegerField(default=0, choices=[(0, b'Fail'), (1, b'Success')])),
                ('text_local_id', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='farmer',
            name='qr_code',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='farmer',
            name='referred_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='farmer',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registrationsms',
            name='farmer',
            field=models.ForeignKey(to='loop.Farmer'),
        ),
        migrations.AddField(
            model_name='registrationsms',
            name='user_created',
            field=models.ForeignKey(related_name='loop_registrationsms_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='registrationsms',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_registrationsms_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
