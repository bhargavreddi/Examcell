from django.contrib import admin

# Register your models here.
from Examination.models import Student, Faculty, Classroom, ClassroomCapacity, Regulation, Year, Semester, Department, \
    ExaminationType, Months, RegisteredStudents, Timetable, InvigilationCount, Arrangement, Examination,Subject, \
    Invigilation

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Classroom)
admin.site.register(ClassroomCapacity)
admin.site.register(Regulation)
admin.site.register(Year)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Department)
admin.site.register(ExaminationType)
admin.site.register(Months)
admin.site.register(Examination)
admin.site.register(RegisteredStudents)
admin.site.register(Timetable)
admin.site.register(Invigilation)
admin.site.register(Arrangement)