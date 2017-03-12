from __future__ import unicode_literals
from django.db import models
# Create your models here.
class Regulation(models.Model):
    regulation = models.CharField(max_length=10)
    def __str__(self):
        return self.regulation
class Department(models.Model):
    name = models.CharField(max_length= 50)
    def __str__(self):
        return self.name
class Year(models.Model):
    year = models.IntegerField(default=1)
    def __str__(self):
        return str(self.year)
class Semester(models.Model):
    semester = models.IntegerField(default=1)
    def __str__(self):
        return str(self.semester)
class Student(models.Model):
    student_id = models.CharField(max_length=20 , primary_key=True)
    student_name = models.CharField(max_length=225)
    student_year = models.ForeignKey(Year)
    student_semester = models.ForeignKey(Semester)
    regulation = models.ForeignKey(Regulation)
    dept = models.ForeignKey(Department)
    def __str__(self):
        return self.student_id
class Faculty(models.Model):
    faculty_id = models.CharField(max_length=20, primary_key=True)
    faculty_name = models.CharField(max_length=225)
    dept = models.ForeignKey(Department)
    def __str__(self):
        return self.faculty_id
class Subject(models.Model):
    subject_code = models.CharField(max_length=20,primary_key=True)
    subject_name = models.CharField(max_length=225)
    regulation = models.ForeignKey(Regulation)
    drawingType = models.BooleanField(default=False)
    def __str__(self):
        return self.subject_code
class ClassroomCapacity(models.Model):
    size = models.IntegerField(default=24)
    def __str__(self):
        return str(self.size)
class Classroom(models.Model):
    classroom_number = models.CharField(max_length=20,primary_key=True)
    dept = models.ForeignKey(Department)
    capacity = models.ForeignKey(ClassroomCapacity)
    def __str__(self):
        return self.capacity
class ExaminationType(models.Model):
    type = models.CharField(max_length=30)
    def __str__(self):
        return self.type
class Months(models.Model):
    month = models.CharField(max_length=30)
    def __str__(self):
        return self.month
class Examination(models.Model):
    examination_name = models.CharField(max_length=225)
    type = models.CharField(max_length=30)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    def __str__(self):
        return self.examination_name
class RegisteredStudents(models.Model):
    student = models.ForeignKey(Student)
    subject = models.ForeignKey(Subject)
    regulation = models.ForeignKey(Regulation)
    type = models.ForeignKey(ExaminationType)
    examination = models.ForeignKey(Examination)
    class Meta:
        unique_together = (("student","subject","examination"),)
class Timetable(models.Model):
    date = models.DateField()
    subject = models.ForeignKey(Subject)
    examination = models.ForeignKey(Examination)
    regulation = models.ForeignKey(Regulation)
    set_number = models.IntegerField(default=1)
    max_set = models.IntegerField(default=1)
    class Meta:
        unique_together = (("date","subject"),)
class InvigilationCount(models.Model):
    faculty = models.ForeignKey(Faculty)
    remaining = models.IntegerField(default=0)
    assigned = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
class Invigilation(models.Model):
    examination = models.ForeignKey(Examination)
    classroom = models.ForeignKey(Classroom)
    faculty = models.ForeignKey(Faculty)
    status = models.CharField(max_length=50)
    class Meta:
        unique_together = (("examination","classroom","faculty"),)
class Arrangement(models.Model):
    examination = models.ForeignKey(Examination)
    classroom = models.ForeignKey(Classroom)
    student = models.ForeignKey(Student)
    date = models.DateField()
    subject = models.ForeignKey(Subject)
    time = models.TimeField()
    set_number = models.IntegerField()
    malpractice = models.BooleanField()
    blankomr = models.BooleanField()
    attendance = models.BooleanField()
    class Meta:
        unique_together = (("examination","student","date","subject"),)