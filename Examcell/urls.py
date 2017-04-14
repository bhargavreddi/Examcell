"""Examcell URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from Examcell import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/get_departments/$',views.getDepartments),
    url(r'^api/login/$',views.login),
    url(r'^api/get_regulations/$',views.getRegulations),
    url(r'^api/list_student_register/$',views.registerStudentList),
    url(r'^api/get_years/$',views.getYears),
    url(r'^api/get_semesters/$',views.getSemesters),
    url(r'^api/get_examinations/$',views.getExaminations),
    url(r'^api/promote/$',views.promoteStudents),
    url(r'^api/demote/$',views.demoteStudents),
    url(r'^api/upload_student_list/$',views.uploadStudentList),
    url(r'^api/upload_faculty_timetable/$',views.uploadFacultyTimetable),
    url(r'^api/upload_timetable/$',views.uploadTimetable),
    url(r'^api/delete_register_students/(?P<pk>[0-9]*)/$',views.removeRegisterStudents),
    url(r'^api/delete_timetable/(?P<pk>[0-9]*)/$',views.removeTimetable),
    url(r'^api/getTimings/(?P<id>[0-9]*)/$',views.getExaminationsTimings),
    url(r'^api/checkExam/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/$',views.checkExam),
    url(r'^api/isArranged/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/$',views.isArranged),
    url(r'^api/getCapacity/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/$',views.getCapacity),
    url(r'^api/getClassrooms/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/$',views.getClassrooms),
    url(r'^api/arrangeStudents/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/$',views.arrangeStudents),
    url(r'^api/retreiveClassrooms/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/$',views.retreiveClassrooms),
    url(r'^api/retreiveSubjects/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/$',views.retreiveSubjects),
    url(r'^api/studentsClassroom/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/(?P<cs>.*)/$',views.studentsClassroom),
    url(r'^api/studentsSubject/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/(?P<sub_code>.*)/$',views.studentsSubject),
    url(r'^api/isSetAllocated/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/$',views.isSetAllocated),
    url(r'^api/setSubjects/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/$',views.setSubjects),
    url(r'^api/getStudentDetails/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/(?P<regno>.*)/$',views.getStudentDetails),
    url(r'^api/getInvigilationDetails/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/$',views.getInvigilationDetails),
    url(r'^api/forceInvigilation/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/(?P<faculty>.*)/$',views.forceInvigilation),
    url(r'^api/changeInvigilation/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/(?P<faculty>.*)/$',views.changeInvigilation),
    url(r'^api/acceptInvigilation/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/(?P<faculty>.*)/$',views.acceptInvigilation),
    url(r'^api/rejectInvigilation/(?P<id>[0-9]*)/(?P<yyyy>\d*)/(?P<mm>\d*)/(?P<dd>\d*)/(?P<hh>\d*)/(?P<min>\d*)/(?P<faculty>.*)/$',views.rejectInvigilation),
]