from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Examination.serializer import StudentSerializer, DepartmentSerializer, RegulationSerializer
from Examination.models import Student, Department, Regulation, Year, Semester
# Create your views here.
@api_view(['PUT'])
def addStudent(request):
    """
    Retrieve, update or delete a snippet instance.
    """
    if request.method == 'PUT':
        data = request.data
        student_id = data.get('student_id')
        student_name = data.get('student_name')
        dept = data.get('dept')
        year = data.get('year')
        semester = data.get('semester')
        regulation = data.get('regulation')
        dept_obj = Department.objects.all().get(name=dept)
        regulation_obj = Regulation.objects.all().get(regulation = regulation)
        obj = Student(student_id = student_id,student_name=student_name,dept=dept_obj,student_year = year,student_semester = semester,regulation = regulation_obj )
        obj.save()
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
@api_view(['POST'])
def addStudentList(request):
    if request.method == 'POST':
        from openpyxl import load_workbook
        file = request.FILES.get('file')
        workbook = load_workbook(file)
        # Getting List of All Departments
        sheet_list = workbook.sheetnames
        def getDeptList(sheet_name):
            sheet = workbook[sheet_name]
            row = 2
            while True:
                if sheet.cell(row=row, column=1).value == None:
                    break
                hallticket = sheet.cell(row=row, column=2).value
                year = sheet.cell(row = row,column=5).value
                semester = sheet.cell(row=row, column=6).value
                try:
                    Student.objects.all().get(student_id=hallticket)
                except Exception:
                    obj = Student()
                    obj.student_id = hallticket
                    obj.student_name = hallticket
                    obj.regulation = Regulation.objects.all().get(regulation = 'R13')
                    obj.student_year = Year.objects.all().get(year=year)
                    obj.student_semester = Semester.objects.all().get(semester=semester)
                    obj.dept = Department.objects.all().get(name='Computer Science and Engineering')
                    obj.save()
                row = row + 1
        for sheet in sheet_list:
            getDeptList(sheet)
        pass
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