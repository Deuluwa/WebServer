from deuluwa.models import User, Userinformation, Courseinformation, Attendancerecord, Course, Notice
from rest_framework import serializers

class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notice
        fields = ('index', 'message', 'user', 'date', 'time')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'admin')


class UserInformationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Userinformation
        fields = ('id', 'address', 'phonenumber', 'name')

class CourseInformationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Courseinformation
        fields = ('coursename', 'classday', 'startdate', 'enddate', 'starttime', 'coursetime')

class AttendanceRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendancerecord
        fields = ('index','userid','courseid','checkdate','checktime')

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('index', 'lectureindex', 'lectureroomindex')