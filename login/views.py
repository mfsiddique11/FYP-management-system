from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from login.models import UserProfile
from login.models import Project
from .models import Meeting
from .models import Document
from .models import Role
from .models import Designation, Doclocation, Isconfirmed, Calendar
import datetime
# Create your views here.


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            request.session['username'] = user.username
            if user.userprofile.role_id_id == 1:
                auth.login(request, user)
                return redirect('stddashboard')
            elif user.userprofile.role_id_id == 3:
                auth.login(request, user)
                return redirect('hoddashboard')
            elif user.userprofile.role_id_id == 2:
                auth.login(request, user)
                return redirect('supervisordashboard')
            elif user.userprofile.role_id_id == 5:
                auth.login(request, user)
                return redirect('fypcoordinatordashboard')
            elif user.userprofile.role_id_id == 4:
                auth.login(request, user)
                return redirect('fypteamdashboard')
            else:
                return render(request, 'login/index.html')
        else:
            error = "Invalid username or password"
            return render(request, 'login/index.html', {'error': error})

    else:
        return render(request, 'login/index.html')


def stddashboard(request):
    c1 = 0
    c2 = 0
    devs = []
    docs = []
    doclocs = []
    statuses=[]
    reviews=[]
    date=[]
    supervisor = ''
    projecttitle = ''
    projectdescription = ''
    projectcreated = ''
    cdesc = []
    cdat = []
    mdesc = []
    mdat = []
    users3=User.objects.filter(username=request.session['username'])
    for user3 in users3:
            calendars = Calendar.objects.filter(semester__in=[user3.userprofile.semester,0])
            if calendars:
                    for calendar in calendars:
                            cdesc.append(calendar.description)
                            cdat.append(calendar.deadline.strftime("%A %d %B %Y"))

    calendar = zip(cdesc, cdat)
    users2 = User.objects.filter(username=request.session['username'])
    for user2 in users2:
          projects = user2.project_set.all()
          if projects:
                  for project in projects:
                          meetings = project.meeting_set.all()
                          if meetings:
                                  for meeting in meetings:
                                          mdesc.append(meeting.description)
                                          mdat.append(
                                              meeting.deadline.strftime("%A %d %B %Y"))

    meeting = zip(mdesc, mdat)
    users = User.objects.filter(username=request.session['username'])
    for user in users:
        projects = user.project_set.all()
        for project in projects:
            documents = project.documents.all()
            if documents:
                    for document in documents:
                            docs.append(document)
                            locs = Doclocation.objects.filter(
                                project=project, document=document)
                            for loc in locs:
                                    doclocs.append(loc.filelocation)
                                    statuses.append(loc.approved)
                                    reviews.append(loc.reviews)
                                    date.append(loc.created)

            member = project.members.all()
            devs = []
            supervisor = ''
            c1 = 0
            c2 = 0
            for member in member:
                if member.userprofile.role_id_id == 1:
                    devs.append(member)
                elif member.userprofile.role_id_id == 2:
                    supervisor = member

                c1 = c1+1
                status = Isconfirmed.objects.filter(
                    project=project, user=member)
                for s in status:
                    if s.status == True:
                        c2 = c2+1

            if c1 == c2:
                projecttitle = project.title
                projectdescription = project.description
                projectcreated = project.created
                documents = zip(doclocs, docs,statuses,reviews,date)
                return render(request, 'students/stddashboard.html', {'meeting': meeting, 'calendar': calendar, 'documents': documents, 'supervisor': supervisor, 'devs': devs, 'projecttitle': projecttitle, 'projectdescription': projectdescription, 'projectcreated': projectcreated})
            else:
                    error = "Project proposal approval pending"
                    return render(request, 'students/stddashboard.html', {'error': error, 'meeting': meeting, 'calendar': calendar, })
    error = 'please submit your proposal'
    return render(request, 'students/stddashboard.html', {'error': error, 'meeting': meeting, 'calendar': calendar, })


def stdnotification(request):
    check = 0
    users = User.objects.filter(username=request.session['username'])
    projecttitles = []
    for user in users:
        projects = user.project_set.all()
        for project in projects:
            status = Isconfirmed.objects.filter(project=project, user=user)
            for s in status:
                if s.status == None:

                    projecttitles.append(project.title)
                else:
                        check = 1

        if check == 1:
                return render(request, 'students/stdnotification.html')
        else:
                return render(request, 'students/stdnotification.html', {'projecttitles': projecttitles})

def stdchangepassword(request):
        if request.method == 'POST':
                oldpass = request.POST['oldpassword']
                newpass = request.POST['newpassword']
                confirmpass = request.POST['confirmpassword']
                users = auth.authenticate(username=request.session['username'], password=oldpass)

                if users is not None:
                                if newpass==confirmpass:
                                        u = User.objects.get(username__exact=request.session['username'])
                                        u.set_password(newpass)
                                        u.save()
                                        success='Password Updated' 
                                        return render(request, 'students/stdchangepassword.html', {'success': success}) 
                                       
                                else:
                                        error="Passwords donot match" 
                                        return render(request, 'students/stdchangepassword.html', {'error': error})
                else:
                        error="wrong pass"
                        return render(request, 'students/stdchangepassword.html', {'error': error})

        return render(request, 'students/stdchangepassword.html')



def stdprojectform(request):

    students = []
    supervisors = []
    users = User.objects.exclude(username=request.session['username'])
    uss=User.objects.filter(username=request.session['username'])
    for us in uss:
            sem=us.userprofile.semester
    for user in users:
            if not user.project_set.all():
                    if user.userprofile.role_id_id == 1 and user.userprofile.semester==sem:
                            students.append(user)

                    elif user.userprofile.role_id_id == 2:
                            supervisors.append(user)

            elif user.project_set.all().count() < 3 and user.userprofile.role_id_id == 2:
                    print(user.project_set.all().count())
                    supervisors.append(user)

    if request.method == 'POST':
        print('ssssssssssssss')

        users = User.objects.filter(username=request.session['username'])
        for user in users:
            projects = user.project_set.all()

            if projects:

                for project in projects:
                    status = Isconfirmed.objects.filter(
                        project=project, user=user)
                    for s in status:
                        if s.status == True:
                            error = "You have already submited a proposal or have accepted one."
                            return render(request, 'students/stdprojectform.html', {'error': error, 'students': students, 'supervisors': supervisors})
                        elif s.status == None:
                            error = "someone have submitted a proposal having you as a member, Please check notifications."
                            return render(request, 'students/stdprojectform.html', {'error': error, 'students': students, 'supervisors': supervisors})

            else:
                    p_title = request.POST['title']
                    p_des = request.POST['description']
                    if p_title == '':
                            error = "Title is required"
                            return render(request, 'students/stdprojectform.html', {'error': error, 'students': students, 'supervisors': supervisors})
                    if p_des == '':
                            error = "Description is required"
                            return render(request, 'students/stdprojectform.html', {'error': error, 'students': students, 'supervisors': supervisors})

                    p_spr = request.POST['supervisor']
                #     if request.POST['member1']:
                #         p_m1 = request.POST['member1']
                #     if request.POST['member2']:
                #         p_m2 = request.POST['member2']
                #     if request.POST['member3']:
                #         p_m3 = request.POST['member3']
                    hod = ''
                    project = Project(title=p_title, description=p_des)
                    project.save()

                    for user in users:
                        confirm = Isconfirmed(
                            project=project, user=user, status=True)
                        confirm.save()
                    if 'member1' in request.POST:
                        p_m1 = request.POST['member1']
                        if p_m1 != 'none':
                            users = User.objects.filter(username=p_m1)
                            for user in users:
                                    confirm = Isconfirmed(
                                        project=project, user=user, status=None)
                                    confirm.save()
                    if 'member2' in request.POST:
                        p_m2 = request.POST['member2']
                        if p_m2 != 'none':
                            users = User.objects.filter(username=p_m2)
                            for user in users:
                                    confirm = Isconfirmed(
                                        project=project, user=user, status=None)
                                    confirm.save()
                    if 'member3' in request.POST:
                        p_m3 = request.POST['member3']
                        if p_m3 != 'none':
                            users = User.objects.filter(username=p_m3)
                            for user in users:
                                    confirm = Isconfirmed(
                                        project=project, user=user, status=None)
                                    confirm.save()

                    users = User.objects.filter(username=p_spr)
                    for user in users:
                        confirm = Isconfirmed(
                            project=project, user=user, status=None)
                        confirm.save()

                    users = User.objects.all()
                    for user in users:
                        if user.userprofile.role_id_id == 3:
                            confirm = Isconfirmed(
                                project=project, user=user, status=None)
                            confirm.save()
                    success = "Submitted successfully, please wait for others to accept."
                    return render(request, 'students/stdprojectform.html', {'success': success, 'students': students, 'supervisors': supervisors})
    return render(request, 'students/stdprojectform.html', {'students': students, 'supervisors': supervisors})




def stduploadfile(request):
    documentss=[]
    docs=Document.objects.all()
    print(docs)  
    for doc in docs:
            documentss.append(doc.name)
            
    if request.method == 'POST':
        check=0
        c1=0
        c2=0
        doctype=request.POST['type']
        filelocation=request.FILES['file']
        users = User.objects.filter(username=request.session['username'])
        for user in users:
            projects = user.project_set.all()
            if projects:
                for project in projects:
                        users2=project.members.all()
                        for user2 in users2:
                                c1=c1+1
                                status = Isconfirmed.objects.filter(project=project, user=user2)
                                for s in status:
                                        if s.status == True:
                                                c2=c2+1
                        if c1==c2:
                                # documents=project.documents.all()
                                # if documents:
                                        documents=Document.objects.all()
                                        for document in documents:
                                                 if document.name==doctype:
                                                         confirm = Doclocation(project=project, document=document, filelocation=filelocation)
                                                         confirm.save()
                                                         success="Uploaded successfully"
                                                         return render(request, 'students/stduploadfile.html', {'success':success,'documentss':documentss})

                                #         for document in documents:
                                #                 if document.name==doctype:
                                #                         check=1
                                                        
                                #                         locc=Doclocation.objects.filter(project=project, document=document)
                                #                         for loc in locc:
                                #                                 import os
                                #                                 from django.conf import settings
                                #                                 os.remove(os.path.join(settings.MEDIA_ROOT,str(loc.filelocation) ))
                                #                         Doclocation.objects.filter(project=project, document=document).delete()        
                                #                         confirm = Doclocation(project=project, document=document, filelocation=filelocation)
                                #                         confirm.save()    
                                #                         success="Updated successfully"
                                #                         return render(request, 'students/stduploadfile.html', {'success':success,'documentss':documentss})
                                                        
                                #         if check==0:
                                #                 documents=Document.objects.all()
                                #                 for document in documents:
                                #                         if document.name==doctype:
                                #                                 confirm = Doclocation(project=project, document=document, filelocation=filelocation)
                                #                                 confirm.save()
                                #                                 success="Uploaded successfully"
                                #                                 return render(request, 'students/stduploadfile.html', {'success':success,'documentss':documentss})
                                
                                # else:
                                         
                        else:
                                error="your project has not been approved by everyone, please wait for approval."
                                return render(request, 'students/stduploadfile.html', {'error':error,'documentss':documentss})

            else:
                    error="Please submit project proposal first."
                    return render(request, 'students/stduploadfile.html', {'error':error,'documentss':documentss})

    return render(request, 'students/stduploadfile.html', {'documentss':documentss})



def stdfiledelete(request):
        if request.method == 'POST':
                docname = request.POST['docname']
                locc=Doclocation.objects.filter(filelocation=docname)
                for loc in locc:
                        import os
                        from django.conf import settings
                        os.remove(os.path.join(settings.MEDIA_ROOT,str(loc.filelocation) ))
                Doclocation.objects.filter(filelocation=docname).delete()  
        return redirect('stddashboard')

def stdaccept(request):
    if request.method == 'POST':
        title = request.POST['title']
        users = User.objects.filter(username=request.session['username'])
        for user in users:
            projects = Project.objects.filter(title=title)
            for project in projects:
                Isconfirmed.objects.filter(
                    project=project, user=user).update(status=True)
                return redirect('stdnotification')


def stdreject(request):
    if request.method == 'POST':
        title = request.POST['title']
        users = User.objects.filter(username=request.session['username'])
        for user in users:
            projects = Project.objects.filter(title=title)
            for project in projects:
                Isconfirmed.objects.filter(
                    project=project).delete()
                Project.objects.filter(title=project.title).delete()
                return redirect('stdnotification')



def spraccept(request):
    if request.method == 'POST':
        title = request.POST['title']
        users = User.objects.filter(username=request.session['username'])
        for user in users:
            projects = Project.objects.filter(title=title)
            for project in projects:
                Isconfirmed.objects.filter(
                    project=project, user=user).update(status=True)
                return redirect('supervisornotification')


def sprreject(request):
    if request.method == 'POST':
        title = request.POST['title']
        users = User.objects.filter(username=request.session['username'])
        for user in users:
            projects = Project.objects.filter(title=title)
            for project in projects:
                Isconfirmed.objects.filter(
                    project=project).delete()
                Project.objects.filter(title=project.title).delete()
                return redirect('supervisornotification')





def hodaccept(request):
    if request.method == 'POST':
        title = request.POST['title']
        users = User.objects.filter(username=request.session['username'])
        for user in users:
            projects = Project.objects.filter(title=title)
            for project in projects:
                Isconfirmed.objects.filter(
                    project=project, user=user).update(status=True)
                return redirect('hodnotification')


def hodreject(request):
    if request.method == 'POST':
        title = request.POST['title']
        users = User.objects.filter(username=request.session['username'])
        for user in users:
            projects = Project.objects.filter(title=title)
            for project in projects:
                Isconfirmed.objects.filter(
                    project=project).delete()
                Project.objects.filter(title=project.title).delete()
                return redirect('hodnotification')


def filereject(request):
    if request.method == 'POST':
        title = request.POST['name']
        remarks=request.POST['remarks']
        locc = Doclocation.objects.filter(filelocation=title)
        for loc in locc:
            loc.approved=False
            loc.reviews=remarks
            loc.save()
        return redirect('supervisornotification')

def fileaccept(request):
    if request.method == 'POST':
        title = request.POST['name']
        remarks=request.POST['remarks']
        locc = Doclocation.objects.filter(filelocation=title)
        for loc in locc:
            loc.approved=True
            loc.reviews=remarks
            loc.save()
        return redirect('supervisornotification')

def stdnotificationdetail(request):
    if request.method == 'POST':
        p_title = request.POST['title']
        devs = []
        supervisor = ''
        projecttitle = ''
        projectdescription = ''
        projectcreated = ''
        projects = Project.objects.filter(title=p_title)

        for project in projects:
            members = project.members.all()
            print(members)
            devs = []
            supervisor = ''
            for member in members:
                if member.userprofile.role_id_id == 1:
                    devs.append(member)
                elif member.userprofile.role_id_id == 2:
                    supervisor = member

            projecttitle = project.title
            projectdescription = project.description
            projectcreated = project.created
            return render(request, 'students/stdnotificationdetail.html', {'supervisor': supervisor, 'devs': devs, 'projecttitle': projecttitle, 'projectdescription': projectdescription, 'projectcreated': projectcreated})

    return render(request, 'students/stdnotification.html')




def supervisordashboard(request):
    hodcheck=0
    sprcheck=0
    check=0
    users = User.objects.filter(username=request.session['username'])
    projecttitles = []
    for user in users:
        projects = user.project_set.all()
        for project in projects:
            users2=project.members.all()
            for user2 in users2:
                    status = Isconfirmed.objects.filter(project=project, user=user2)
                    if user2.userprofile.role_id_id == 2:
                            for s in status:
                                    if s.status == True:
                                            sprcheck=1
                    elif user2.userprofile.role_id_id == 3:
                            for s in status:
                                    if s.status == True:
                                            hodcheck=1
                    if hodcheck==1 and sprcheck==1:
                            projecttitles.append(project.title)
                            sprcheck=0
                            hodcheck=0
                            check=1

        if check==0:
                events=Meeting.objects.all()
                for event in events:
                        if event.deadline < datetime.date.today():
                                event.delete()   
                return render(request, 'supervisor/supervisordashboard.html')
        else:
                events=Meeting.objects.all()
                for event in events:
                        if event.deadline < datetime.date.today():
                                event.delete()
                return render(request, 'supervisor/supervisordashboard.html', {'projecttitles': projecttitles})


def supervisorchangepassword(request):
        if request.method == 'POST':
                oldpass = request.POST['oldpassword']
                newpass = request.POST['newpassword']
                confirmpass = request.POST['confirmpassword']
                users = auth.authenticate(username=request.session['username'], password=oldpass)

                if users is not None:
                                if newpass==confirmpass:
                                        u = User.objects.get(username__exact=request.session['username'])
                                        u.set_password(newpass)
                                        u.save()
                                        success='Password Updated' 
                                        return render(request, 'supervisor/supervisorchangepassword.html', {'success': success}) 
                                       
                                else:
                                        error="Passwords donot match" 
                                        return render(request, 'supervisor/supervisorchangepassword.html', {'error': error})
                else:
                        error="wrong pass"
                        return render(request, 'supervisor/supervisorchangepassword.html', {'error': error})

        return render(request, 'supervisor/supervisorchangepassword.html')



def supervisornotification(request):
    stdcheck=0
    sprcheck=0
    check=0
    users = User.objects.filter(username=request.session['username'])
    projecttitles = []
    docs=[]
    docs2=[]
    for user in users:
        projects = user.project_set.all()
        for project in projects:
            users2=project.members.all()
            for user2 in users2:
                    status = Isconfirmed.objects.filter(project=project, user=user2)
                    if user2.userprofile.role_id_id == 1:
                            for s in status:
                                    if s.status != True:
                                            stdcheck=1
                    elif user2.userprofile.role_id_id == 2:
                            for s in status:
                                    if s.status == None:
                                            sprcheck=1

            if stdcheck==0 and sprcheck==1:
                    projecttitles.append(project.title)
                    sprcheck=0
                    check=1
            else:
                    stdcheck=0

        if check==0:
                users = User.objects.filter(username=request.session['username'])
                for user in users:
                        projects = user.project_set.all()
                        for project in projects:
                                documents=project.documents.all()
                                for document in documents:
                                        locc=Doclocation.objects.filter(project=project, document=document,approved=None)
                                        for loc in locc:
                                                docs.append(document.name)
                                                docs2.append(loc.filelocation)
                        documents = zip(docs, docs2)                        

                return render(request, 'supervisor/supervisornotification.html',{'documents':documents})
        else:
                users = User.objects.filter(username=request.session['username'])
                for user in users:
                        projects = user.project_set.all()
                        for project in projects:
                                documents=project.documents.all()
                                for document in documents:
                                        locc=Doclocation.objects.filter(project=project, document=document,approved=None)
                                        for loc in locc:
                                                docs.append(document.name)
                                                docs2.append(loc.filelocation)
                        documents = zip(docs, docs2)                         
                return render(request, 'supervisor/supervisornotification.html', {'projecttitles': projecttitles,'documents':documents})





def hodnotificationdetail(request):
    if request.method == 'POST':
        p_title = request.POST['title']
        devs = []
        supervisor = ''
        projecttitle = ''
        projectdescription = ''
        projectcreated = ''
        projects = Project.objects.filter(title=p_title)

        for project in projects:
            members = project.members.all()
            devs = []
            supervisor = ''
            for member in members:
                if member.userprofile.role_id_id == 1:
                    devs.append(member)
                elif member.userprofile.role_id_id == 2:
                    supervisor = member

            projecttitle = project.title
            projectdescription = project.description
            projectcreated = project.created
            return render(request, 'hod/hodnotificationdetail.html', {'supervisor': supervisor, 'devs': devs, 'projecttitle': projecttitle, 'projectdescription': projectdescription, 'projectcreated': projectcreated})

    return render(request, 'hod/hodnotification.html')



def hodchangepassword(request):
        if request.method == 'POST':
                oldpass = request.POST['oldpassword']
                newpass = request.POST['newpassword']
                confirmpass = request.POST['confirmpassword']
                users = auth.authenticate(username=request.session['username'], password=oldpass)

                if users is not None:
                                if newpass==confirmpass:
                                        u = User.objects.get(username__exact=request.session['username'])
                                        u.set_password(newpass)
                                        u.save()
                                        success='Password Updated' 
                                        return render(request, 'hod/hodchangepassword.html', {'success': success}) 
                                       
                                else:
                                        error="Passwords donot match" 
                                        return render(request, 'hod/hodchangepassword.html', {'error': error})
                else:
                        error="wrong pass"
                        return render(request, 'hod/hodchangepassword.html', {'error': error})

        return render(request, 'hod/hodchangepassword.html')



def hodprojectdetail(request):
    if request.method == 'POST':
        p_title = request.POST['title']
        devs = []
        docs=[]
        doclocs=[]
        supervisor = ''
        projecttitle = ''
        projectdescription = ''
        projectcreated = ''
        projects = Project.objects.filter(title=p_title)

        for project in projects:
            documents=project.documents.all()
            if documents:
                    for document in documents:
                        if document.name=='srs' or document.name=='sds' or document.name=='report': 
                            
                            locs = Doclocation.objects.filter(project=project, document=document,approved=True)
                            for loc in locs:
                                    docs.append(document)
                                    doclocs.append(loc.filelocation)    
            members = project.members.all()
            devs = []
            supervisor = ''
            for member in members:
                if member.userprofile.role_id_id == 1:
                    devs.append(member)
                elif member.userprofile.role_id_id == 2:
                    supervisor = member

            projecttitle = project.title
            projectdescription = project.description
            projectcreated = project.created
            documents = zip(doclocs, docs)
            return render(request, 'hod/hodprojectdetail.html', {'documents':documents,'supervisor': supervisor, 'devs': devs, 'projecttitle': projecttitle, 'projectdescription': projectdescription, 'projectcreated': projectcreated})

    return render(request, 'hod/hoddashbaord.html')



def supervisorprojectdetail(request):
    if request.method == 'POST':
        p_title = request.POST['title']
        devs = []
        docs=[]
        doclocs=[]
        supervisor = ''
        projecttitle = ''
        projectdescription = ''
        projectcreated = ''
        projects = Project.objects.filter(title=p_title)

        for project in projects:
            documents=project.documents.all()
            if documents:
                    for document in documents:
                            
                            
                            locs = Doclocation.objects.filter(project=project, document=document,approved=True)
                            for loc in locs:
                                    docs.append(document)
                                    doclocs.append(loc.filelocation)    
            members = project.members.all()
            devs = []
            supervisor = ''
            c1 = 0
            c2 = 0
            for member in members:
                if member.userprofile.role_id_id == 1:
                    devs.append(member)
                elif member.userprofile.role_id_id == 2:
                    supervisor = member

            projecttitle = project.title
            projectdescription = project.description
            projectcreated = project.created
            documents = zip(doclocs, docs)
            return render(request, 'supervisor/supervisorprojectdetail.html', {'documents':documents,'supervisor': supervisor, 'devs': devs, 'projecttitle': projecttitle, 'projectdescription': projectdescription, 'projectcreated': projectcreated})

    return render(request, 'supervisor/supervisordashbaord.html')








def hoddashboard(request):
    check=0
    users = User.objects.filter(username=request.session['username'])
    projecttitles = []
    for user in users:
        projects = user.project_set.all()
        for project in projects:
                    status = Isconfirmed.objects.filter(project=project, user=user)
                    for s in status:
                            if s.status == True:
                                    projecttitles.append(project.title)
                                    check=1

        if check==0:
                return render(request, 'hod/hoddashboard.html')
        else:
                return render(request, 'hod/hoddashboard.html', {'projecttitles': projecttitles})




def hodnotification(request):
    stdcheck=0
    sprcheck=0
    hodcheck=0
    check=0
    users = User.objects.filter(username=request.session['username'])
    projecttitles = []
    for user in users:
        projects = user.project_set.all()
        for project in projects:
            users2=project.members.all()
            for user2 in users2:
                    status = Isconfirmed.objects.filter(project=project, user=user2)
                    if user2.userprofile.role_id_id == 1:
                            for s in status:
                                    if s.status != True:
                                            stdcheck=1
                    elif user2.userprofile.role_id_id == 2:
                            for s in status:
                                    if s.status != True:
                                            sprcheck=1
                    elif user2.userprofile.role_id_id == 3:  
                             for s in status:
                                    if s.status == None:
                                            hodcheck=1  


            if stdcheck==0 and sprcheck==0 and hodcheck==1:
                    projecttitles.append(project.title)
                    hodcheck=0
                    check=1
            else:
                    sprcheck=0
                    stdcheck=0

        if check==0:
                return render(request, 'hod/hodnotification.html')
        else:
                return render(request, 'hod/hodnotification.html', {'projecttitles': projecttitles})



def supervisormeeting(request):



    hodcheck=0
    sprcheck=0
    check=0
    users = User.objects.filter(username=request.session['username'])
    projectss = []
    for user in users:
        projects = user.project_set.all()
        if projects:

                for project in projects:
                        users2=project.members.all()
                        for user2 in users2:
                                status = Isconfirmed.objects.filter(project=project, user=user2)
                                if user2.userprofile.role_id_id == 2:
                                        for s in status:
                                                if s.status == True:
                                                        sprcheck=1
                                elif user2.userprofile.role_id_id == 3:
                                        for s in status:
                                                if s.status == True:
                                                        hodcheck=1
                                if hodcheck==1 and sprcheck==1:
                                        projectss.append(project.title)
                                        sprcheck=0
                                        hodcheck=0
                                        check=1

                if check==0:
                        error="your project has been waiting approval by Hod."
                        return render(request, 'supervisor/supervisormeeting.html',{'error':error,'projectss': projectss })
        

        else:
                error="You have taken no projects, please check notifications."
                return render(request, 'supervisor/supervisormeeting.html',{'error':error,'projectss': projectss})

    if request.method == 'POST':
        p_title = request.POST['project']
        desc = request.POST['description']
        date = request.POST['date']
        print(date)
        if p_title=='none':
                error="Please select a project."
                return render(request, 'supervisor/supervisormeeting.html', {'error':error,'projectss': projectss,'desc':desc,'date':date})
        if desc=='':
                error="Description is required"
                return render(request, 'supervisor/supervisormeeting.html', {'error':error,'projectss': projectss})
        
        if str(datetime.date.today()) <= date:
                projects=Project.objects.filter(title=p_title)
                for project in projects:
                        confirm=Meeting(description=desc,deadline=date,project=project)
                        confirm.save()
                        success="event has been set successfully."
                        return render(request, 'supervisor/supervisormeeting.html', {'success':success,'projectss': projectss})
        else:
                error='chose todays or higher date'
                return render(request, 'supervisor/supervisormeeting.html', {'error':error,'projectss': projectss,'desc':desc})

    return render(request, 'supervisor/supervisormeeting.html',{'projectss': projectss})





def supervisornotificationdetail(request):
    if request.method == 'POST':
        p_title = request.POST['title']
        c1 = 0
        c2 = 0
        devs = []
        supervisor = ''
        projecttitle = ''
        projectdescription = ''
        projectcreated = ''
        projects = Project.objects.filter(title=p_title)
        print(projects)

        for project in projects:
            members = project.members.all()
            print(members)
            devs = []
            supervisor = ''
            c1 = 0
            c2 = 0
            for member in members:
                if member.userprofile.role_id_id == 1:
                    devs.append(member)
                elif member.userprofile.role_id_id == 2:
                    supervisor = member

            #      c1=c1+1
            #      status=Isconfirmed.objects.filter(project=project,user=member)
            #      for s in status:
            #              if s.status==True:
            #                      c2=c2+1

        #      if c1==c2:
            projecttitle = project.title
            projectdescription = project.description
            projectcreated = project.created
            return render(request, 'supervisor/supervisornotificationdetail.html', {'supervisor': supervisor, 'devs': devs, 'projecttitle': projecttitle, 'projectdescription': projectdescription, 'projectcreated': projectcreated})

    return render(request, 'supervisor/supervisornotification.html')














def supervisorfiledetail(request):
    if request.method == 'POST':
        docname = request.POST['name']
        documents = Doclocation.objects.filter(filelocation=docname)
        print(documents)
        for document in documents:
                doc=document.filelocation
                return render(request, 'supervisor/supervisorfiledetail.html', {'doc':doc})

    return render(request, 'supervisor/supervisornotification.html')


















def fypcoordinatordashboard(request):
    if request.method == 'POST':
            desc = request.POST['description']
            date = request.POST['date'] 
            sem = request.POST['semester'] 
            if str(datetime.date.today()) <= date:
                     confirm=Calendar(description=desc,deadline=date,semester=sem)
                     confirm.save()
                     success="event set successfully"
                     return render(request, 'fypcoordinator/fypcoordinatordashboard.html',{'success':success})
            else:
                    error="date should be today or higher"
                    return render(request, 'fypcoordinator/fypcoordinatordashboard.html',{'error':error,'desc':desc,'sem':sem})
    events=Calendar.objects.all()
    for event in events:
            if event.deadline < datetime.date.today():
                    event.delete()     
    return render(request, 'fypcoordinator/fypcoordinatordashboard.html')


def fypcoordinatorchangepassword(request):
        if request.method == 'POST':
                oldpass = request.POST['oldpassword']
                newpass = request.POST['newpassword']
                confirmpass = request.POST['confirmpassword']
                users = auth.authenticate(username=request.session['username'], password=oldpass)

                if users is not None:
                                if newpass==confirmpass:
                                        u = User.objects.get(username__exact=request.session['username'])
                                        u.set_password(newpass)
                                        u.save()
                                        success='Password Updated' 
                                        return render(request, 'fypcoordinator/fypcoordinatorchangepassword.html', {'success': success}) 
                                       
                                else:
                                        error="Passwords donot match" 
                                        return render(request, 'fypcoordinator/fypcoordinatorchangepassword.html', {'error': error})
                else:
                        error="wrong pass"
                        return render(request, 'fypcoordinator/fypcoordinatorchangepassword.html', {'error': error})

        return render(request, 'fypcoordinator/fypcoordinatorchangepassword.html')


def fypcoordinatoreventlist(request):
    
    events = Calendar.objects.all()
    eventsdescription = []
    for event in events:
            eventsdescription.append(event.description)
    return render(request, 'fypcoordinator/fypcoordinatoreventlist.html', {'eventsdescription': eventsdescription})


def fypcoordinatordeleteevent(request):
        if request.method == 'POST':
                e_des = request.POST['description']
                events = Calendar.objects.filter(description=e_des).delete()
                return redirect('fypcoordinatoreventlist')





def fypcoordinatoreventdetail(request):
    if request.method == 'POST':
        e_des = request.POST['description']
        events = Calendar.objects.filter(description=e_des)
        for event in events:
            eventdescription = event.description
            semester = event.semester
            date=event.deadline
            return render(request, 'fypcoordinator/fypcoordinatoreventdetail.html', {'eventdescription':eventdescription,'semester':semester,'date':date})
    else:   
            if request.session['message']=='1':
                    e_des = request.session['des']
                    events = Calendar.objects.filter(description=e_des)
                    for event in events:
                            eventdescription = event.description
                            semester = event.semester
                            date=event.deadline
                            success='event updated'
                            return render(request, 'fypcoordinator/fypcoordinatoreventdetail.html', {'eventdescription':eventdescription,'semester':semester,'date':date,'success':success})
            elif request.session['message']=='0':
                    e_des = request.session['rdes']
                    events = Calendar.objects.filter(description=e_des)
                    for event in events:
                            eventdescription = event.description
                            semester = event.semester
                            date=event.deadline
                            error='chose todays date or higher'
                            return render(request, 'fypcoordinator/fypcoordinatoreventdetail.html', {'eventdescription':eventdescription,'semester':semester,'date':date,'error':error})
            
                

def fypcoordinatoreventupdate(request):
    if request.method == 'POST':
            desc = request.POST['description']
            rdesc = request.POST['rdescription']
            request.session['rdes'] = rdesc
            request.session['des'] = desc
            date = request.POST['date'] 
            sem = request.POST['semester'] 
            events=Calendar.objects.filter(description=rdesc)
            for event in events:
                    if str(datetime.date.today()) <= date:
                            event.description=desc
                            event.deadline=date
                            event.semester=sem
                            event.save()
                            request.session['message'] = '1'
                            return redirect('fypcoordinatoreventdetail')
                    else:
                            request.session['message'] = '0'
                            return redirect('fypcoordinatoreventdetail')
                    

                    





def fypteamdashboard(request):
    a=0
    c1=0
    c2=0
    check=0
    projecttitles = []
    projects=Project.objects.all()
    for project in projects:
            
            users=project.members.all()
            for user in users:
                    c1=c1+1
                    status = Isconfirmed.objects.filter(project=project, user=user)
                    for s in status:
                            if s.status == True:
                                    c2=c2+1
            
            if c1==c2:
                    projecttitles.append(project.title)
                    c1=0
                    c2=0
                    check=1
            else:
                    c1=0
                    c2=0        
    if check==0:
             return render(request, 'fypteam/fypteamdashboard.html')
    else:
             return render(request, 'fypteam/fypteamdashboard.html', {'projecttitles': projecttitles})




def fypteamprojectdetail(request):
    if request.method == 'POST':
        p_title = request.POST['title']
        c1 = 0
        c2 = 0
        devs = []
        docs=[]
        doclocs=[]
        supervisor = ''
        projecttitle = ''
        projectdescription = ''
        projectcreated = ''
        projects = Project.objects.filter(title=p_title)
        print(projects)

        for project in projects:
            documents=project.documents.all()
            if documents:
                    print('a')
                    for document in documents:
                        print(document.name)
                        if document.name=='srs' or document.name=='sds' or document.name=='report':       
                            print('i')
                            
                            locs = Doclocation.objects.filter(project=project, document=document,approved=True)
                            for loc in locs:
                                    docs.append(document.name)
                                    doclocs.append(loc.filelocation)
            members = project.members.all()
            print(members)
            devs = []
            supervisor = ''
            c1 = 0
            c2 = 0
            for member in members:
                if member.userprofile.role_id_id == 1:
                    devs.append(member)
                elif member.userprofile.role_id_id == 2:
                    supervisor = member

            projecttitle = project.title
            projectdescription = project.description
            projectcreated = project.created
            print(doclocs)
            documents = zip(doclocs, docs)
            return render(request, 'fypteam/fypteamprojectdetail.html', {'documents':documents,'supervisor': supervisor, 'devs': devs, 'projecttitle': projecttitle, 'projectdescription': projectdescription, 'projectcreated': projectcreated})

    return render(request, 'fypteam/fypteamdashbaord.html')





def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')

















def  supervisoreventlist(request):
    eventsdescription = []    
    users=User.objects.filter(username=request.session['username'])
    for user in users:
          projects = user.project_set.all()
          if projects:
                  for project in projects:
                          meetings = project.meeting_set.all()
                          if meetings:
                                  for meeting in meetings:
                                          eventsdescription.append(meeting.description)
                  return render(request, 'supervisor/supervisoreventlist.html', {'eventsdescription': eventsdescription})


def supervisordeleteevent(request):
        if request.method == 'POST':
                e_des = request.POST['description']
                events = Meeting.objects.filter(description=e_des).delete()
                return redirect('supervisoreventlist')





def  supervisoreventdetail(request):
    
    if request.method == 'POST':
        e_des = request.POST['description']
        events = Meeting.objects.filter(description=e_des)
        for event in events:
            projecttitles=[]
            eventdescription = event.description
            users=User.objects.filter(username=request.session['username'])
            for user in users:

                    projects = user.project_set.exclude(title=event.project.title)
                    if projects:
                            for project in projects: 
                                    projecttitles.append(project.title)  

            project=event.project.title
            date=event.deadline
            return render(request, 'supervisor/supervisoreventdetail.html', {'eventdescription':eventdescription,'project':project,'date':date,'projecttitles':projecttitles})
    else:   
            if request.session['message']=='1':
                    e_des = request.session['des']
                    events = Meeting.objects.filter(description=e_des)
                    for event in events:
                            eventdescription = event.description
                            
                            date=event.deadline
                            success='event updated'
                            users=User.objects.filter(username=request.session['username'])
                            projecttitles=[]
                            for user in users:
                                    projects = user.project_set.exclude(title=event.project.title)
                                    if projects:
                                           for project in projects:
                                                   projecttitles.append(project.title)   
                            project = event.project.title                                                
                            return render(request, 'supervisor/supervisoreventdetail.html', {'eventdescription':eventdescription,'project':project,'projecttitles':projecttitles,'date':date,'success':success})
            elif request.session['message']=='0':
                    e_des = request.session['rdes']
                    events = Meeting.objects.filter(description=e_des)
                    print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
                    for event in events:
                            eventdescription = event.description
                            
                            date=event.deadline
                            error='chose todays date or higher'
                            projecttitles=[]
                            users=User.objects.filter(username=request.session['username'])
                            for user in users:
                                    projects = user.project_set.exclude(title=event.project.title)
                                    if projects:
                                           for project in projects: 
                                                   projecttitles.append(project.title) 
                            project = event.project.title                          
                            return render(request, 'supervisor/supervisoreventdetail.html', {'eventdescription':eventdescription,'project':project,'projecttitles':projecttitles,'date':date,'error':error})
            
                

def  supervisoreventupdate(request):
    if request.method == 'POST':
            desc = request.POST['description']
            rdesc = request.POST['rdescription']
            request.session['rdes'] = rdesc
            request.session['des'] = desc
            date = request.POST['date'] 
            project = request.POST['project'] 
            events=Meeting.objects.filter(description=rdesc)
            for event in events:
                    if str(datetime.date.today()) <= date:
                            event.description=desc
                            event.deadline=date
                            projects=Project.objects.filter(title=project)
                            for project in projects:
                                    print(project.id)
                                    event.project_id=project.id
                            event.save()
                            request.session['message'] = '1'
                            print('yyyyyyyyyy')
                            return redirect('supervisoreventdetail')
                    else:
                            request.session['message'] = '0'
                            print('rr')
                            return redirect('supervisoreventdetail')
                    

                    


