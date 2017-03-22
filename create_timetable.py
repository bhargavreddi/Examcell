

__author__ = 'Bhargav'
import django
import sys,os
sys.path.append("/home/bhargav/Examcell")
sys.path.append("/home/mvgrexamcell/Examcell")
os.environ["DJANGO_SETTINGS_MODULE"] = "Examcell.settings"
django.setup()
from Examination.models import Subject,Examination,Regulation,Timetable
examination = Examination.objects.get(examination_name = '4-2 II Mid Examination 2017')
regulation = Regulation.objects.get(regulation = 'R13')
Timetable.objects.all().delete()
time = "9:30"
subject_codes = ["RT42051","RT42052","RT42043E","RT42053A"]
date = ["2017-04-03","2017-04-04","2017-04-05","2017-04-06"]
index= 0 
for subject_code in subject_codes:
	subject = Subject.objects.get(subject_code = subject_code)
	obj = Timetable()
	obj.date = date[index]
	obj.subject = subject
	obj.time = time
	obj.examination = examination
	obj.regulation = regulation
	obj.save()
	index = index + 1


