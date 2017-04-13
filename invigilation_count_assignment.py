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
                assigned = 0
                total = 10
                remaining = total
            elif assigned > total:
                total = 10 - (assigned - total)
                assigned = 0
                remaining = total
            else:
                total = 10 + (total - assigned)
                assigned = 0
                remaining = total
            obj.remaining = remaining
            obj.assigned = assigned
            obj.total = total
            obj.save()
        except Exception:
            obj = InvigilationCount()
            obj.faculty = Faculty.objects.get(faculty_id=faculty_tuple[0])
            obj.assigned = 0
            obj.total = 10
            obj.remaining = obj.total
            obj.save()
# InvigilationCount.objects.all().delete()
yearRollUp()
