from django.contrib.auth.models import User
from django.db import models

SCORE_CHOICES = (
	('0','0'),
	('1','1'),
	('2','2'),
	('3','3'),
	)

VIDEO_GRADE = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

APPROVAL = (
	('0', 'No'),
	('1', 'Yes'),
	)

ADOPTED = (
	('0', 'No'),
	('1', 'Yes'),
	)

EQUIPMENT_WORK = (
	('0', 'Not Working'),
	('1', 'Working'),
	)

DATA_UPDATE_SCREENING_CHOICES = (
	('1', 'lag/gap <= 7 days (3)'),
	('2', 'lag/gap <= 7 days (2)'),
	('3', 'lag/gap <= 21 days (1)'),
	('4', 'lag/gap  7 days (0)'),
	)


DATA_UPDATE_ADOPTION_CHOICES = (
	('1', 'lag/gap <= 7 days (3)'),
	('2', 'lag/gap <= 7 days (2)'),
	('3', 'lag/gap <= 21 days (1)'),
	('4', 'lag/gap  7 days (0)'),
	)


DATA_ENTERED_QUALITY_SCREENING_CHOICES = (
	('1', 'Complete & accurate entries (3)'),
	('2', 'Few Minor errors - wrong time mentioned, spelling mistakes (2)'),
	('3', 'Significant errors - wrong entries of VO/Person/SHG/Date/Video (1)'),
	)


DATA_ENTERED_QUALITY_ADOPTION_CHOICES = (
	('1', 'Complete & accurate entries (3)'),
	('2', 'Few Minor errors - wrong time mentioned, spelling mistakes (2)'),
	('3', 'Significant errors - wrong entries of VO/Person/SHG/Date/Video (1)'),
	)

GRADE = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

VERIFIED_BY_CHOICES = (
    ('0', 'Digital Green'),
    ('1', 'Partner'),
)


class QACocoModel(models.Model):
    user_created = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_created", editable = False, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_modified = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_related_modified",editable = False, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
