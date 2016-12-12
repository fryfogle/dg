# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loop', '0006_auto_20161212_0823'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregatorIncentive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('start_date', models.DateField()),
                ('model_type', models.IntegerField(default=0, choices=[(0, b'Direct'), (1, b'Tax Based'), (2, b'Slab Based')])),
                ('aggregator', models.ForeignKey(to='loop.LoopUser')),
            ],
        ),
        migrations.CreateModel(
            name='IncentiveModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postfix_expression', models.CharField(max_length=100)),
                ('infix_expression', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IncentiveParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notation', models.CharField(max_length=3)),
                ('parameter_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Slab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lower_band', models.IntegerField()),
                ('upper_band', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='gaddidar',
            name='commission',
            field=models.FloatField(default=1.0, verbose_name=b'Discount'),
        ),
        migrations.AlterField(
            model_name='gaddidarcommission',
            name='discount_percent',
            field=models.FloatField(default=0.0, verbose_name=b'Discount', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='gaddidarcommission',
            name='gaddidar',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'mandi', to='loop.Gaddidar', chained_field=b'mandi'),
        ),
        migrations.AlterField(
            model_name='gaddidarshareoutliers',
            name='mandi',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'assigned_mandis', to='loop.Mandi', chained_field=b'aggregator'),
        ),
        migrations.AddField(
            model_name='aggregatorincentive',
            name='incentive_model',
            field=models.ForeignKey(to='loop.IncentiveModel'),
        ),
        migrations.AddField(
            model_name='aggregatorincentive',
            name='slab',
            field=models.ForeignKey(to='loop.Slab'),
        ),
        migrations.AddField(
            model_name='aggregatorincentive',
            name='user_created',
            field=models.ForeignKey(related_name='loop_aggregatorincentive_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='aggregatorincentive',
            name='user_modified',
            field=models.ForeignKey(related_name='loop_aggregatorincentive_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='aggregatorincentive',
            unique_together=set([('start_date', 'aggregator', 'model_type', 'incentive_model')]),
        ),
    ]
