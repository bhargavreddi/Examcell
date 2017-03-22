from rest_framework import serializers, viewsets
from Examination.models import Student, Department, Regulation, Year, Semester, Examination, ExaminationType, Months


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('student_id','student_name', 'student_year', 'student_semester', 'dept','regulation')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id','name')

class RegulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regulation
        fields = ('id','regulation')

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ('id','year')

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('id','semester')

class ExaminationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExaminationType
        fields = ('id','type')

class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Months
        fields = ('id','month')

class ExaminationSerializer(serializers.HyperlinkedModelSerializer):
    month = MonthSerializer()
    type = ExaminationTypeSerializer()
    class Meta:
        model = Examination
        fields = ('id','type','examination_name','month','year')