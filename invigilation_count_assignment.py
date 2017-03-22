__author__ = 'Bhargav'
import django
import sys,os
sys.path.append("/home/bhargav/Examcell")
sys.path.append("/home/mvgrexamcell/Examcell")
os.environ["DJANGO_SETTINGS_MODULE"] = "Examcell.settings"
django.setup()
from Examination.models import InvigilationCount, Faculty


def yearRollUp():
    faculty_list = Faculty.objects.all().values_list('faculty_id')

    for faculty_tuple in faculty_list:
        try:
            obj = InvigilationCount.objects.get(faculty=faculty_tuple[0])
            remaining = obj.remaining
            assigned = obj.assigned
            total = obj.total

            if(assigned == total):
                remaining = 0
                assigned = 0
                total = 10
            elif assigned > total:
                remaining = 0
                total = 10 - (assigned - total)
                assigned = 0
            else:
                remaining = 0
                total = 10 + (total - assigned)
                assigned = 0
            obj.remaining = remaining
            obj.assigned = assigned
            obj.total = total
            obj.save()
        except Exception:
            obj = InvigilationCount()
            obj.faculty = Faculty.objects.get(faculty_id=faculty_tuple[0])
            obj.remaining = 0
            obj.assigned = 0
            obj.total = 10
            obj.save()

yearRollUp()
