__author__ = 'Bhargav'
import django
import sys,os
sys.path.append("/home/bhargav/Examcell")
sys.path.append("/home/mvgrexamcell/Examcell")
os.environ["DJANGO_SETTINGS_MODULE"] = "Examcell.settings"
django.setup()
from Examination.models import FacultyTimetable, Faculty, InvigilationCount, Invigilation, Examination

time1 = "10:00"
time2 = "13:00"
day = "Monday"
exam = ['III']
limit = 10


time = ["9:00","9:50","10:40","11:30","12:20","13:10","14:00","14:50","15:40"]
def compare(time1,time2):
    time_array1 = time1.split(":")
    time_array2 = time2.split(":")

    if int(time_array1[0]) > int(time_array2[0]):
        return True
    elif int(time_array1[0]) == int(time_array2[0]):
        if int(time_array1[1]) == int(time_array2[1]):
            return False
        elif int(time_array1[1]) > int(time_array2[1]):
            return True
        else:
            return False
    else:
        return False
def inIndex(t):
    index = 0
    values = range(len(time))
    for i in values:
        if(compare(t,time[i]) == False):
            index = i
            break
    else:
        return 7
    return index

def outIndex(t):
    index = 0
    values = range(len(time))
    values.reverse()
    for i in values:
        if(compare(t,time[i]) == True):
            index = i
            break
    else:
        return 7
    return index



def allocateInvigilation(time1,time2,day,year,limit,examination_id):
    fac_list = FacultyTimetable.objects.filter(day__day = day).values()
    indices = {0:'hour1',1:'hour2',2:'hour3',3:'hour4',4:'hour5',5:'hour6',6:'hour7',7:'hour8'}
    index1= outIndex(time1)
    index2 = inIndex(time2)
    count = 0
    faculty_list = []
    flag = True
    for d in fac_list:
        flag = True
        for i in range(index1,index2):
            try:
                array = d[indices[i]].split('-')
                array = array[1]
            except Exception:
                array = 'None'
            if (d[indices[i]] == 'Free' or array in exam):
                pass
            else:
                flag = False
        if (flag):
            fac_obj_count = InvigilationCount.objects.get(faculty__faculty_id=d['faculty_id'])
            inv_count = Invigilation.objects.filter(faculty__faculty_id=d['faculty_id'],examination = Examination.objects.get(id = examination_id)).count()
            if fac_obj_count.remaining != 0 and inv_count <2 :
                faculty_list.append(d['faculty_id'])
                count = count + 1
            if count == limit:
                break

    if count < limit:
        for d in fac_list:
            if d['faculty_id'] in faculty_list:
                pass
            else:
                inv_count = Invigilation.objects.filter(faculty__faculty_id=d['faculty_id'],
                                                        examination=Examination.objects.get(id=examination_id)).count()
                if inv_count < 2:
                    faculty_list.append(d['faculty_id'])
                    count = count + 1
            if count == limit:
                break
        else:
            for d in fac_list:
                if d['faculty_id'] in faculty_list:
                    pass
                else:
                    faculty_list.append(d['faculty_id'])
                    count = count + 1
                if count == limit:
                    break
    return faculty_list

print allocateInvigilation(time1,time2,day,exam,limit,1)
