import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import django.utils.timezone

class EventTemplate(models.Model):

    class YEARGROUPS(models.IntegerChoices):
        year_nine = 9
        year_ten = 10
        year_eleven = 11
        year_twelve = 12
        year_thirteen = 13

    template_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=40)
    year_group = models.IntegerField(choices=YEARGROUPS.choices)
    maximum_capacity = models.IntegerField()

class Schedule(models.Model):

    schedule_id = models.AutoField(primary_key=True)
    session = models.CharField(max_length=20)
    day = models.CharField(max_length=20, default=datetime.datetime.now().strftime("%A"))
    template_id = models.ForeignKey(EventTemplate, on_delete=models.CASCADE)

# 'Models' where classes are tables / relations and attributes or variables are columns / fields
class EventInstance(models.Model):

    # Columns / Fields
    event_id = models.AutoField(primary_key=True)
    event_date = models.DateTimeField()
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE)

class Student(models.Model):

    # Choices [Tuples or Enumerations]
    BOARDINGHOUSES = [
        ('TS', 'Tsavo'),
        ('TU', 'Turkana'),
        ('L' ,'Laikipia'),
        ('B', 'Baringo'),
        ('S', 'Samburu'),
    ]

    class YEARGROUPS(models.IntegerChoices):
        year_nine = 9
        year_ten = 10
        year_eleven = 11
        year_twelve = 12
        year_thirteen = 13


    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    # Columns / Fields
    student_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank= True, null=True, on_delete=models.CASCADE)
    student_first_name = models.CharField(max_length=30)
    student_last_name = models.CharField(max_length=30)
    boarding_house = models.CharField(max_length=30, choices=BOARDINGHOUSES)
    year_group = models.IntegerField(choices=YEARGROUPS.choices)
    gender = models.CharField(max_length=30, choices=GENDERS)


class Registration(models.Model):
    # Choices [Tuples or Enumerations]

    # Columns / Fields
    registration_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    event_id = models.ForeignKey(EventInstance, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

class RegistrationRecord(models.Model):

    # Columns / Fields
    
    # User Information Not Necessary, if user deleted then record should be deleted
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    
    # The specific event instance information
    registration_id = models.IntegerField()
    event_id = models.ForeignKey(EventInstance, on_delete=models.CASCADE)
    event_date = models.DateTimeField()
    
    # Registration information
    registration_date = models.DateTimeField()
    day = models.CharField(max_length=20, default=datetime.datetime.now().strftime("%A"))
    session = models.CharField(max_length=20)
    
    # The events information
    template_id = models.IntegerField()
    schedule_id = models.IntegerField()
    event_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=40)
    year_group = models.IntegerField()
    maximum_capacity = models.IntegerField()

    creation_date = models.DateTimeField(auto_now_add=True)

    # e.g. 1 18 Monday Morning 14 19  20 Basketball Boys 12 
    # 1: Jasiri Wa-kyendo and if this accountis deleted then all my RegistrationRecords should be deleted through on_delete=models.CASCADE 
    