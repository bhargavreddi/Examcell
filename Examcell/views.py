import json

from django.http.response import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Examination.serializer import StudentSerializer, DepartmentSerializer, RegulationSerializer, YearSerializer, \
    SemesterSerializer, ExaminationSerializer
from Examination.models import Student, Department, Regulation, Year, Semester, Examination, FacultyTimetable, Faculty, \
    Day, Timetable, Subject, RegisteredStudents, ExaminationType, Classroom, Arrangement, ClassroomCapacity


@api_view(['GET'])
def removeRegisterStudents(request,pk):
    if pk !=None:
        RegisteredStudents.objects.all().filter(examination__id=pk).delete()
        data = {
            'status': 'success'
        }
        return JsonResponse(data)
    data = {
        'status': 'failed'
    }
    return JsonResponse(data)

@api_view(['GET'])
def removeTimetable(request,pk):
    if pk !=None:
        Timetable.objects.all().filter(examination__id=pk).delete()
        data = {
            'status': 'success'
        }
        return JsonResponse(data)
    data = {
        'status': 'failed'
    }
    return JsonResponse(data)

@api_view(['GET'])
def getDepartments(request):
    if request.method == 'GET':
        snippet = Department.objects.all()
        serializer = DepartmentSerializer(snippet, many=True)
        return Response(serializer.data)
@api_view(['GET'])
def getRegulations(request):
    if request.method == 'GET':
        snippet = Regulation.objects.all()
        serializer = RegulationSerializer(snippet, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getYears(request):
    if request.method == 'GET':
        snippet = Year.objects.all()
        serializer = YearSerializer(snippet, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getSemesters(request):
    if request.method == 'GET':
        snippet = Semester.objects.all()
        serializer = SemesterSerializer(snippet, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getExaminations(request):
    if request.method == 'GET':
        snippet = Examination.objects.all()
        serializer = ExaminationSerializer(snippet, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def promoteStudents(request):
    if request.method == 'POST':
        data = request.data
        dept = data.get('department')
        year = data.get('year')
        sem = data.get('semester')
        obj = Student.objects.all().filter(dept__name=dept,student_year__year=year,student_semester__semester=sem).values_list('student_id')
        if sem == 2:
            if year == 4:
                return HttpResponseNotFound()
            year = year + 1
            sem = 1
        else:
            sem = 2

        for id_tuple in obj:
            id = id_tuple[0]
            student = Student.objects.get(student_id = id)
            student.student_year = Year.objects.get(year=year)
            student.student_semester = Semester.objects.get(semester=sem)
            student.save()
        return HttpResponse()

@api_view(['POST'])
def demoteStudents(request):
    if request.method == 'POST':
        data = request.data
        dept = data.get('department')
        year = data.get('year')
        sem = data.get('semester')
        obj = Student.objects.all().filter(dept__name=dept,student_year__year=year,student_semester__semester=sem).values_list('student_id')
        if sem == 1:
            if year == 1:
                return HttpResponseNotFound()
            year = year - 1
            sem = 2
        else:
            sem = 1

        for id_tuple in obj:
            id = id_tuple[0]
            student = Student.objects.get(student_id = id)
            student.student_year = Year.objects.get(year=year)
            student.student_semester = Semester.objects.get(semester=sem)
            student.save()
        return HttpResponse()

@api_view(['POST'])
def uploadStudentList(request):
    if request.method == 'POST':
        from openpyxl import  load_workbook
        file = request.FILES.get('file')
        workbook = load_workbook(file)
        sheet_list = workbook.sheetnames
        dept_names = {'cse': 'Computer Science and Engineering','eee' : 'Electrical & Electronics Engineering','ece':'Electronics and Communication Engineering','it': 'Information Technology','mech':'Mechanical Engineering','chem':'Chemical Engineering','civil':'Civil Engineering'}
        for sheet_name in sheet_list:
            sheet = workbook[sheet_name]
            row = 2
            while True:
                if sheet.cell(row=row, column=1).value == None:
                    break
                regno = sheet.cell(row=row, column=2).value
                student_name = sheet.cell(row=row, column=3).value
                regulation = sheet.cell(row=row,column=7).value
                obj = Student()
                obj.student_id = regno
                obj.student_name = student_name
                obj.student_year = Year.objects.all().get(year='1')
                obj.student_semester = Semester.objects.all().get(semester='1')
                obj.regulation = Regulation.objects.all().get(regulation=regulation)
                obj.dept = Department.objects.all().get(name=dept_names[sheet_name])
                obj.save()
                row = row + 1
        data = {
            'status': 'success'
        }
        return JsonResponse(data)

@api_view(['POST'])
def registerStudentList(request):
    if request.method == 'POST':
        from openpyxl import load_workbook
        file = request.FILES.get('file')
        exam_name = file.__str__().split('.')
        exam_name = exam_name[0]
        RegisteredStudents.objects.all().filter(examination__examination_name=exam_name).delete()
        workbook = load_workbook(file)
        # Getting List of All Departments
        sheet_list = workbook.sheetnames
        dept_names = {'cse': 'Computer Science and Engineering', 'eee': 'Electrical & Electronics Engineering',
                          'ece': 'Electronics and Communication Engineering', 'it': 'Information Technology',
                          'mech': 'Mechanical Engineering', 'chem': 'Chemical Engineering', 'civil': 'Civil Engineering'}
        for sheet_name in sheet_list:
            sheet = workbook[sheet_name]
            row = 2
            while True:
                if sheet.cell(row=row, column=1).value == None:
                    break
                hallticket = sheet.cell(row=row, column=2).value
                year = sheet.cell(row = row,column=5).value
                semester = sheet.cell(row=row, column=6).value
                subject_code = sheet.cell(row=row,column=7).value
                regulation = sheet.cell(row=row,column=4).value
                type = sheet.cell(row = row,column=3).value
                try:
                    obj = RegisteredStudents()
                    obj.student = Student.objects.get(student_id=hallticket)
                    obj.subject = Subject.objects.get(subject_code=subject_code)
                    obj.regulation = Regulation.objects.get(regulation=regulation)
                    obj.type = ExaminationType.objects.get(type = type )
                    obj.examination = Examination.objects.get(examination_name=exam_name)
                    obj.save()
                except Exception:
                    data ={
                        'status' : 'failed'
                    }
                    return JsonResponse(data)
                row = row + 1

        data = {
            'status': 'success'
        }
        return JsonResponse(data)

@api_view(['POST'])
def uploadFacultyTimetable(request):
    from openpyxl import load_workbook
    file = request.FILES.get('file')
    # Opening the workbook
    workbook = load_workbook(file)
    sheet1 = workbook['Sheet1']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    FacultyTimetable.objects.all().delete()
    row = 1
    column = 1
    while True:
        while True:
            cell = sheet1.cell(row=row, column=column)
            if cell.value != None:

                faculty_name = cell.value
                if (faculty_name == 'DR B SRINIVAS'):
                    pass
                day = [None, None, None, None, None, None, None, None, None]
                for i in range(1, 7):
                    obj = FacultyTimetable()
                    try:
                        obj.faculty = Faculty.objects.get(faculty_name=faculty_name)
                    except Exception:
                        data = {
                            'status': 'failed'
                        }
                        return JsonResponse(data)
                    obj.day = Day.objects.get(day=days[i - 1])
                    day[1] = sheet1.cell(row=row + i, column=column + 1).value
                    if day[1] is None or day[1] == ' ':
                        day[1] = 'Free'
                    obj.hour1 = day[1]
                    day[2] = sheet1.cell(row=row + i, column=column + 2).value
                    if day[2] is None or day[2] == ' ':
                        if sheet1.cell(row=row + i,
                                       column=column + 1).coordinate in sheet1.merged_cells and sheet1.cell(row=row + i,
                                                                                                            column=column + 2).coordinate in sheet1.merged_cells:
                            day[2] = day[1]
                        else:
                            day[2] = 'Free'
                    obj.hour2 = day[2]
                    day[3] = sheet1.cell(row=row + i, column=column + 3).value
                    if day[3] is None or day[3] == ' ':
                        if sheet1.cell(row=row + i,
                                       column=column + 2).coordinate in sheet1.merged_cells and sheet1.cell(row=row + i,
                                                                                                            column=column + 3).coordinate in sheet1.merged_cells:
                            day[3] = day[2]
                        else:
                            day[3] = 'Free'
                    obj.hour3 = day[3]
                    day[4] = sheet1.cell(row=row + i, column=column + 4).value
                    if day[4] is None or day[4] == ' ':
                        if sheet1.cell(row=row + i,
                                       column=column + 3).coordinate in sheet1.merged_cells and sheet1.cell(row=row + i,
                                                                                                            column=column + 4).coordinate in sheet1.merged_cells:
                            day[4] = day[3]
                        else:
                            day[4] = 'Free'
                    obj.hour4 = day[4]
                    day[5] = sheet1.cell(row=row + i, column=column + 5).value
                    if day[5] is None or day[5] == ' ':
                        if sheet1.cell(row=row + i,
                                       column=column + 4).coordinate in sheet1.merged_cells and sheet1.cell(row=row + i,
                                                                                                            column=column + 5).coordinate in sheet1.merged_cells:
                            day[5] = day[4]
                        else:
                            day[5] = 'Free'
                    obj.hour5 = day[5]
                    day[6] = sheet1.cell(row=row + i, column=column + 6).value
                    if day[6] is None or day[6] == ' ':
                        if sheet1.cell(row=row + i,
                                       column=column + 5).coordinate in sheet1.merged_cells and sheet1.cell(row=row + i,
                                                                                                            column=column + 6).coordinate in sheet1.merged_cells:
                            day[6] = day[5]
                        else:
                            day[6] = 'Free'
                    obj.hour6 = day[6]
                    day[7] = sheet1.cell(row=row + i, column=column + 7).value
                    if day[7] is None or day[7] == ' ':
                        if sheet1.cell(row=row + i,
                                       column=column + 6).coordinate in sheet1.merged_cells and sheet1.cell(row=row + i,
                                                                                                            column=column + 7).coordinate in sheet1.merged_cells:
                            day[7] = day[6]
                        else:
                            day[7] = 'Free'
                    obj.hour7 = day[7]
                    day[8] = sheet1.cell(row=row + i, column=column + 8).value
                    if day[8] is None or day[8] == ' ':
                        if sheet1.cell(row=row + i,
                                       column=column + 7).coordinate in sheet1.merged_cells and sheet1.cell(row=row + i,
                                                                                                            column=column + 8).coordinate in sheet1.merged_cells:
                            day[8] = day[7]
                        else:
                            day[8] = 'Free'
                    obj.hour8 = day[8]
                    obj.save()
            else:
                row = row + 9
                column = 1
                break
            column = column + 10
        cell = sheet1.cell(row=row, column=column)
        if cell.value == None:
            break
    data = {
        'status': 'success'
    }
    return JsonResponse(data)

@api_view(['POST'])
def uploadTimetable(request):
    from openpyxl import load_workbook
    file = request.FILES.get('file')
    # Opening the workbook
    workbook = load_workbook(file)
    sheet_list = workbook.sheetnames
    for sheet_name in sheet_list:
        sheet = workbook[sheet_name]
        Timetable.objects.all().filter(examination__examination_name=sheet_name).delete()
        row = 2
        column = 1
        while True:
            cell = sheet.cell(row=row, column=column)
            if cell.value == None:
                break
            obj = Timetable()
            obj.date = sheet.cell(row = row,column=column).value
            obj.subject = Subject.objects.get(subject_code=sheet.cell(row = row,column=column + 1).value)
            obj.examination = Examination.objects.get(examination_name=sheet_name)
            obj.regulation = Regulation.objects.get(regulation=sheet.cell(row = row,column=column + 3).value)
            obj.time = sheet.cell(row=row,column=column+4).value
            row = row + 1
            obj.save()
    data = {
        'status': 'success'
    }
    return JsonResponse(data)



@api_view(['GET'])
def checkExam(request,id,yyyy,mm,dd):
    if request.method == 'GET':
        check = "{0}-{1}-{2}".format(yyyy,mm,dd)
        dates = Timetable.objects.filter(examination__id=id).values_list('date')
        for date in dates:
            if str(date[0]) == check:
                data = {
                    'status' : 'true'
                }
                return JsonResponse(data)
        data = {
            'status': 'false'
        }
        return JsonResponse(data)

@api_view(['GET'])
def isArranged(request,id,yyyy,mm,dd,hh,min):
    if request.method == 'GET':
        date = "{0}-{1}-{2}".format(yyyy,mm,dd)
        time = "{0}:{1}".format(hh, min)
        dates = Arrangement.objects.filter(examination__id=id,date=date,time=time).count()
        if dates == 0:
            data = {
                'status' : 'false'
            }
        else:
            data = {
                'status': 'true'
            }
        return JsonResponse(data)

@api_view(['GET'])
def getCapacity(request,id,yyyy,mm,dd,hh,min):
    if request.method == 'GET':
        date = "{0}-{1}-{2}".format(yyyy,mm,dd)
        time = "{0}:{1}".format(hh,min)
        subjects = Timetable.objects.filter(examination__id=id,date=date,time=time).values_list('subject')
        count = 0
        dhcount = 0
        for subject in subjects:
            temp = RegisteredStudents.objects.filter(examination__id=id,subject__subject_code=subject[0]).count()
            obj = Subject.objects.get(subject_code=subject[0])
            if obj.drawingType:
                dhcount = dhcount + temp
                mod = temp % 4
                dhcount = dhcount + 4 - mod
            else:
                count = count + temp
                mod = temp % 4
                count = count + 4 - mod

        data = {
            "capacity" : count,
            "dhcapacity" : dhcount
        }
        return JsonResponse(data)

@api_view(['GET'])
def retreiveClassrooms(request,id,yyyy,mm,dd,hh,min):
    if request.method == 'GET':
        date = "{0}-{1}-{2}".format(yyyy, mm, dd)
        time = "{0}:{1}".format(hh, min)
        classroom_list_tuple = Arrangement.objects.filter(examination__id=id, date=date, time=time).distinct().values_list('classroom')
        classroom = []
        for tuple in classroom_list_tuple:
            size = Classroom.objects.get(classroom_number=tuple[0]).capacity.size
            classroom.append({"classroom":tuple[0],'size' : size})
        data = {}
        data['classroom_list'] = classroom

        return JsonResponse(data)

@api_view(['GET'])
def retreiveSubjects(request,id,yyyy,mm,dd,hh,min):
    if request.method == 'GET':
        date = "{0}-{1}-{2}".format(yyyy, mm, dd)
        time = "{0}:{1}".format(hh, min)
        subject_list_tuple = Arrangement.objects.filter(examination__id=id, date=date, time=time).distinct().values_list('subject')
        subjects = []
        for tuple in subject_list_tuple:
            obj = Subject.objects.get(subject_code=tuple[0])
            time_obj = Timetable.objects.get(subject=obj)
            subjects.append({"subject_code":tuple[0],"subject_name" : obj.subject_name,'max_set' : time_obj.max_set,"start_set" : time_obj.set_number })
        data = {}
        data['subject_list'] = subjects

        return JsonResponse(data)

@api_view(['GET'])
def studentsClassroom(request,id,yyyy,mm,dd,hh,min,cs):
    if request.method == 'GET':
        date = "{0}-{1}-{2}".format(yyyy, mm, dd)
        time = "{0}:{1}".format(hh, min)
        student_list_tuple = Arrangement.objects.filter(examination__id=id, date=date, time=time,classroom__classroom_number=cs).values_list('student','set_number')
        student_list = []
        for tuple in student_list_tuple:
            student_list.append({'regno' : tuple[0],'set_number' : tuple[1]})
        data = {}
        data['student_list'] = student_list
        return JsonResponse(data)


@api_view(['GET'])
def isSetAllocated(request,id,yyyy,mm,dd,hh,min):
    if request.method == 'GET':
        date = "{0}-{1}-{2}".format(yyyy, mm, dd)
        time = "{0}:{1}".format(hh, min)
        count = Timetable.objects.filter(examination__id=id, date=date, time=time,set_number =0).count()
        if count == 0:
            status = {
                'status' : 'true'
            }
        else:
            status = {
                'status': 'false'
            }
        return JsonResponse(status)

@api_view(['POST'])
def setSubjects(request,id,yyyy,mm,dd,hh,min):
    if request.method == 'POST':
        data = request.data
        date = "{0}-{1}-{2}".format(yyyy, mm, dd)
        time = "{0}:{1}".format(hh, min)
        subject_list = data.subjects
        for subject_dict in subject_list:
            try:
                obj = Timetable.objects.get(examination__id=id, date=date, time=time,subject__subject_code=subject_dict['subject'])
                obj.set_number = subject_dict.start_set
                obj.max_set = subject_dict.max_set
                obj.save()
            except Exception:
                status = {
                    'status': 'failed'
                }
                return JsonResponse(status)
        status = {
            'status': 'success'
        }
        return JsonResponse(status)

@api_view(['POST'])
def arrangeStudents(request,id,yyyy,mm,dd,hh,min):
    if request.method == 'POST':
        date = "{0}-{1}-{2}".format(yyyy, mm, dd)
        time = "{0}:{1}".format(hh, min)
        classroom = request.data.get('classrooms')
        drawing_hall = request.data.get('drawinghalls')
        subjects_list = Timetable.objects.filter(examination__id=id, date=date, time=time).values_list('subject')
        dhsubjects =[]
        subjects = []
        for subject in subjects_list:
            obj = Subject.objects.get(subject_code=subject[0])
            if obj.drawingType:
                dhsubjects.append(subject[0])
            else:
                subjects.append(subject[0])
        Arrangement.objects.filter(examination__id=id,date=date,time=time).delete()
        hall_fill = 0
        try:
            hall_size = Classroom.objects.get(classroom_number=drawing_hall[0]).capacity.size
            hall = drawing_hall[0]
            for dhsubject in dhsubjects:
                depts = Department.objects.values_list('name')
                for dept in depts:
                    list = RegisteredStudents.objects.filter(examination__id=id, subject__subject_code=dhsubject,student__dept__name=dept[0]).values_list('student')
                    for student in list:
                        obj = Arrangement()
                        obj.student = Student.objects.get(student_id=student[0])
                        obj.classtroom = Classroom.objects.get(classroom_number=hall)
                        obj.examination = Examination.objects.get(id = id)
                        obj.date = date
                        obj.time = time
                        obj.subject = Subject.objects.get(subject_code=dhsubject)
                        obj.save()
                        hall_fill =hall_fill + 1
                        if hall_size == hall_fill:
                            hall_fill = 0
                            del drawing_hall[0]
                            hall_size = Classroom.objects.get(classroom_number=drawing_hall[0]).capacity.size
                            hall = drawing_hall[0]
        except Exception:
            pass

        hall_fill = 0
        insert_values = 0
        try:
            hall_size = Classroom.objects.get(classroom_number=classroom[0]).capacity.size
            hall = classroom[0]
            for dhsubject in subjects:
                depts = Department.objects.values_list('name')
                for dept in depts:
                    list = RegisteredStudents.objects.filter(examination__id=id, subject__subject_code=dhsubject,
                                                             student__dept__name=dept[0]).values_list('student')
                    for student in list:
                        obj = Arrangement()
                        obj.student = Student.objects.get(student_id=student[0])
                        obj.classroom = Classroom.objects.get(classroom_number=hall)
                        obj.examination = Examination.objects.get(id=id)
                        obj.date = date
                        obj.time = time
                        obj.subject = Subject.objects.get(subject_code=dhsubject)
                        obj.set_number = 0
                        obj.malpractice = False
                        obj.blankomr = False
                        obj.attendance = True
                        obj.save()
                        hall_fill = hall_fill + 1
                        insert_values = insert_values + 1
                        if hall_size == hall_fill:
                            hall_fill = 0
                            del classroom[0]
                            hall_size = Classroom.objects.get(classroom_number=classroom[0]).capacity.size
                            hall = classroom[0]
                    if insert_values != 0:
                        temp = 4 - insert_values % 4
                        insert_values = 0
                        for i in range(temp):
                            obj = Arrangement()
                            obj.student = Student.objects.get(student_id='100')
                            obj.classroom = Classroom.objects.get(classroom_number=hall)
                            obj.examination = Examination.objects.get(id=id)
                            obj.date = date
                            obj.time = time
                            obj.subject = Subject.objects.get(subject_code=dhsubject)
                            obj.set_number = 0
                            obj.malpractice = False
                            obj.blankomr = False
                            obj.attendance = True
                            obj.save()
        except Exception as e:
            pass

        status = {
            'status' : 'success'
        }
        return JsonResponse(status)

@api_view(['GET'])
def getClassrooms(request,id,yyyy,mm,dd,hh,min):
    if request.method == 'GET':
        date = "{0}-{1}-{2}".format(yyyy, mm, dd)
        time = "{0}:{1}".format(hh, min)
        Arrangement.objects.filter(examination__id=id, date=date, time=time).delete()
        classroom_tuples = Arrangement.objects.filter(date=date,time=time).values_list('classroom')
        classroom_list = []
        for cls in classroom_tuples:
            classroom_list.append(cls[0])

        cls_list = []
        check = Classroom.objects.values_list('classroom_number')
        for classroom in check:
            if classroom[0] in classroom_list:
                pass
            else:
                cls_list.append(classroom[0])
        data = {}
        data['number'] = len(cls_list)
        data['classroom_list'] = []
        for classroom in cls_list:
            obj1 = Classroom.objects.get(classroom_number=classroom)
            size = obj1.capacity.size
            data['classroom_list'].append({'classroom':classroom,'size':size})
        return JsonResponse(data)

@api_view(['GET'])
def getExaminationsTimings(request,id):
    if request.method == 'GET':
        time = Timetable.objects.all().values_list('time').distinct()
        time_list = {}
        time_list['time_list'] = []
        for t in time:
            time_list['time_list'].append({'time':str(t[0])})

        return JsonResponse(time_list)



"""
    if request.method == 'PUT':
        snippet = Image.objects.all()
        serializer = ImageSerializer(snippet,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        student_id = data.get('student_id')
        student_name = data.get('student_name')
        image = Image.objects.get(id = id)
        user = User.objects.get(id=user_id)
        like = Likes.objects.filter(user = user ,image = image)
        if(like.count()==0):
            like = Likes(user = user,image = image)
            like.save()
        else:
            like = Likes.objects.get(user=user, image=image)
            like.delete()
        return Response()
"""