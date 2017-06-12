# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geographies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qacoco', '0002_videoqualityreview_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataEntryVerification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_modified', models.DateTimeField(auto_now=True, null=True)),
                ('data_entry_operator_name', models.CharField(max_length=80, null=True)),
                ('number_of_forms_verfied', models.IntegerField(null=True)),
                ('dataverification_date', models.DateField(null=True, blank=True)),
                ('data_update_screening', models.CharField(max_length=1, null=True, choices=[(b'1', b'lag/gap <= 7 days (3)'), (b'2', b'lag/gap <= 7 days (2)'), (b'3', b'lag/gap <= 21 days (1)'), (b'4', b'lag/gap  7 days (0)')])),
                ('date_update_adoption', models.CharField(max_length=1, null=True, choices=[(b'1', b'lag/gap <= 7 days (3)'), (b'2', b'lag/gap <= 7 days (2)'), (b'3', b'lag/gap <= 21 days (1)'), (b'4', b'lag/gap  7 days (0)')])),
                ('data_entered_quality_screening', models.CharField(max_length=1, null=True, choices=[(b'1', b'Complete & accurate entries (3)'), (b'2', b'Few Minor errors - wrong time mentioned, spelling mistakes (2)'), (b'3', b'Significant errors - wrong entries of VO/Person/SHG/Date/Video (1)')])),
                ('data_entered_quality_adoption', models.CharField(max_length=1, null=True, choices=[(b'1', b'Complete & accurate entries (3)'), (b'2', b'Few Minor errors - wrong time mentioned, spelling mistakes (2)'), (b'3', b'Significant errors - wrong entries of VO/Person/SHG/Date/Video (1)')])),
                ('total_score', models.IntegerField()),
                ('grade', models.CharField(max_length=1, null=True, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C')])),
                ('verified_by', models.CharField(max_length=1, choices=[(b'0', b'Digital Green'), (b'1', b'Partner')])),
                ('remarks', models.TextField(null=True)),
                ('block', models.ForeignKey(to='geographies.Block')),
                ('user_created', models.ForeignKey(related_name='qacoco_dataentryverification_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='qacoco_dataentryverification_related_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'DataEntryVerfication',
                'verbose_name_plural': 'DataEntryVerfications',
            },
        ),
    ]
