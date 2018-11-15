# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Attendancerecord(models.Model):
    index = models.AutoField(primary_key=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    courseid = models.ForeignKey('Course', models.DO_NOTHING, db_column='courseid', blank=True, null=True)
    checkdate = models.DateField()
    checktime = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'attendancerecord'


class Course(models.Model):
    index = models.AutoField(primary_key=True)
    lectureindex = models.ForeignKey('User', models.DO_NOTHING, db_column='lectureindex')
    lectureroomindex = models.ForeignKey('Lectureroom', models.DO_NOTHING, db_column='lectureroomindex')

    class Meta:
        managed = False
        db_table = 'course'


class Courseinformation(models.Model):
    courseindex = models.ForeignKey('Course', models.DO_NOTHING, db_column='courseindex')
    startdate = models.DateField()
    enddate = models.DateField()
    starttime = models.CharField(max_length=4)
    coursetime = models.IntegerField()
    classday = models.CharField(max_length=7)
    coursename = models.TextField()
    index = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'courseinformation'


class Coursestudent(models.Model):
    couseid = models.ForeignKey('Course', models.DO_NOTHING, db_column='couseid')
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    index = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'coursestudent'


class Lectureroom(models.Model):
    index = models.AutoField(primary_key=True)
    nfcid = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'lectureroom'


class Loginsession(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid', primary_key=True)
    value = models.TextField()
    lasttime = models.DateField()

    class Meta:
        managed = False
        db_table = 'loginsession'


class User(models.Model):
    id = models.TextField(primary_key=True)
    password = models.TextField()
    admin = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'user'


class Userinformation(models.Model):
    id = models.ForeignKey(User, models.DO_NOTHING, db_column='id', primary_key=True)
    address = models.TextField(blank=True, null=True)
    phonenumber = models.TextField(blank=True, null=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'userinformation'

class Notice(models.Model):
    index = models.AutoField(primary_key=True)
    message = models.TextField()
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user')
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'notice'