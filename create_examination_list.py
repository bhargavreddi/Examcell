

__author__ = 'Bhargav'
import django
import sys,os
sys.path.append("/home/bhargav/Examcell")
sys.path.append("/home/mvgrexamcell/Examcell")
os.environ["DJANGO_SETTINGS_MODULE"] = "Examcell.settings"
django.setup()
from Examination.models import Subject,Examination,ExaminationType,Student,RegisteredStudents,Regulation
subject_list = Subject.objects.all().values_list('subject_code')
examination = Examination.objects.get(examination_name = '4-2 II Mid Examination 2017')
regulation = Regulation.objects.get(regulation = 'R13')
type = ExaminationType.objects.get(type='Mid Term')
student_list = Student.objects.all().value_list('student_id')

for subject_tuple in subject_list:
	subject = Subject.objects.get(subject_code = subject_tuple[0])
	for student_tuple in student_list:
		student = Student.objects.get(student_id = student_tuple[0])
		obj = RegisteredStudents()
		obj.student = student
		obj.subject = subject
		obj.regulation = regulation
		obj.type = type
		obj.examination = examination
		obj.save()


