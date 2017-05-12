# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'default', max_length=100)),
                ('phonenumber', models.CharField(default=b'0', max_length=14, null=True, blank=True)),
                ('village', models.CharField(default=None, max_length=30, null=True)),
                ('pincode', models.CharField(default=b'0', max_length=8, null=True, blank=True)),
                ('latitude', models.CharField(default=b'0', max_length=15, null=True, blank=True)),
                ('longitude', models.CharField(default=b'0', max_length=15, null=True, blank=True)),
                ('landsize', models.CharField(default=b'0', max_length=5, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('requirementclass', models.IntegerField(choices=[(0, b'Seed'), (1, b'Fertilizer'), (2, b'Loan'), (3, b'Equipments')])),
                ('requirementcrop', models.CharField(default=b'0', max_length=25, null=True, blank=True)),
                ('requirementvariety', models.CharField(default=b'0', max_length=25, null=True, blank=True)),
                ('quantity', models.IntegerField(default=0, null=True, blank=True)),
                ('price', models.FloatField(null=True)),
                ('pickupdate', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('requesttype', models.IntegerField(choices=[(0, b'Personal'), (1, b'Group')])),
                ('requirementclass', models.IntegerField(choices=[(0, b'Seed'), (1, b'Fertilizer'), (2, b'Loan'), (3, b'Equipments')])),
                ('buyrent', models.IntegerField(choices=[(0, b'Buy'), (1, b'Rent')])),
                ('requirementcrop', models.CharField(default=b'0', max_length=25, null=True, blank=True)),
                ('requirementvariety', models.CharField(default=b'0', max_length=25, null=True, blank=True)),
                ('quantity', models.IntegerField(default=0, null=True, blank=True)),
                ('unit', models.IntegerField(choices=[(0, b'Kg'), (1, b'Rupees'), (2, b'Pieces')])),
                ('farmer', models.ForeignKey(to='hack4farming.Farmer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequirementQuotation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('requirementid', models.IntegerField()),
                ('quotationid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'default', max_length=100)),
                ('phonenumber', models.CharField(default=b'0', max_length=14, null=True, blank=True)),
                ('suppliercategory', models.IntegerField(choices=[(0, b'Seed'), (1, b'Fertilizer'), (2, b'Bank'), (3, b'Equipment')])),
                ('firmname', models.CharField(default=b'0', max_length=50, null=True, blank=True)),
                ('pincode', models.CharField(default=b'0', max_length=8, null=True, blank=True)),
                ('latitude', models.CharField(default=b'0', max_length=15, null=True, blank=True)),
                ('longitude', models.CharField(default=b'0', max_length=15, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='quotation',
            name='supplier',
            field=models.ForeignKey(to='hack4farming.Supplier', null=True),
        ),
    ]
