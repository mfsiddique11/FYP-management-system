from django.urls import path

from . import views

urlpatterns = [
     path('',views.index,name='index'),
     path('stdaccept',views.stdaccept,name='stdaccept'),
     path('stdreject',views.stdreject,name='stdreject'),


     path('spraccept',views.spraccept,name='spraccept'),
     path('sprreject',views.sprreject,name='sprreject'),

     path('hodaccept',views.hodaccept,name='hodaccept'),
     path('hodreject',views.hodreject,name='hodreject'),


     path('fileaccept',views.fileaccept,name='fileaccept'),
     path('filereject',views.filereject,name='filereject'),


     path('fypcoordinator/fypcoordinatordashboard',views.fypcoordinatordashboard,name='fypcoordinatordashboard'),
     path('fypcoordinator/fypcoordinatorchangepassword',views.fypcoordinatorchangepassword,name='fypcoordinatorchangepassword'),
     path('fypcoordinator/fypcoordinatoreventlist',views.fypcoordinatoreventlist,name='fypcoordinatoreventlist'),
     path('fypcoordinator/fypcoordinatoreventdetail',views.fypcoordinatoreventdetail,name='fypcoordinatoreventdetail'),
     
     path('fypcoordinatordeleteevent',views.fypcoordinatordeleteevent,name='fypcoordinatordeleteevent'),
     path('fypcoordinatoreventupdate',views.fypcoordinatoreventupdate,name='fypcoordinatoreventupdate'),


     path('hod/hoddashboard',views.hoddashboard,name='hoddashboard'),
     path('hod/hodnotification',views.hodnotification,name='hodnotification'),
     path('hod/hodnotificationdetail',views.hodnotificationdetail,name='hodnotificationdetail'),
     path('hod/hodprojectdetail',views.hodprojectdetail,name='hodprojectdetail'),
     path('hod/hodchangepassword',views.hodchangepassword,name='hodchangepassword'),


     path('supervisor/supervisordashboard',views.supervisordashboard,name='supervisordashboard'),
     path('supervisor/supervisornotification',views.supervisornotification,name='supervisornotification'),
     path('supervisor/supervisornotificationdetail',views.supervisornotificationdetail,name='supervisornotificationdetail'),
     path('supervisor/supervisorfiledetail',views.supervisorfiledetail,name='supervisorfiledetail'),

     path('supervisor/supervisorprojectdetail',views.supervisorprojectdetail,name='supervisorprojectdetail'),
     path('supervisor/supervisormeeting',views.supervisormeeting,name='supervisormeeting'),
     path('supervisor/supervisorchangepassword',views.supervisorchangepassword,name='supervisorchangepassword'),
     path('supervisor/supervisoreventlist',views.supervisoreventlist,name='supervisoreventlist'),
     path('supervisor/supervisoreventdetail',views.supervisoreventdetail,name='supervisoreventdetail'),
     
     path('supervisordeleteevent',views.supervisordeleteevent,name='supervisordeleteevent'),  
     path('supervisoreventupdate',views.supervisoreventupdate,name='supervisoreventupdate'),


     path('students/stdprojectform',views.stdprojectform,name='stdprojectform'),
     path('students/stduploadfile',views.stduploadfile,name='stduploadfile'),
     path('students/stddashboard',views.stddashboard,name='stddashboard'),
     path('students/stdnotification',views.stdnotification,name='stdnotification'),
     path('students/stdnotificationdetail',views.stdnotificationdetail,name='stdnotificationdetail'),
     path('students/stdchangepassword',views.stdchangepassword,name='stdchangepassword'),

     path('stdfiledelete',views.stdfiledelete,name='stdfiledelete'),


     path('fypteam/fypteamdashboard',views.fypteamdashboard,name='fypteamdashboard'),
     path('fypteam/fypteamprojectdetail',views.fypteamprojectdetail,name='fypteamprojectdetail'),
     
     path('logout',views.logout,name='logout'),
     
]