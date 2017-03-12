from rest_framework import serializers, viewsets
from Examination.models import Student, Department, Regulation


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