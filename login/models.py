from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Calendar(models.Model):
        description = models.TextField(null=True, blank=True) 
        semester=models.IntegerField(null=True, blank=True)
        deadline =  models.DateField(null=True, blank=True)  

        def __str__(self):
            template = '{0.description} {0.deadline} {0.semester}'
            return template.format(self)  




class Role(models.Model):
        name = models.CharField(max_length=100,null=True, blank=True)  
        created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
        updated = models.DateTimeField(auto_now=True,null=True, blank=True) 

        def __str__(self):
            template = '{0.name}'
            return template.format(self) 

class Designation(models.Model):
        name = models.CharField(max_length=100,null=True, blank=True)  
        created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
        updated = models.DateTimeField(auto_now=True,null=True, blank=True) 

        def __str__(self):
            template = '{0.name}'
            return template.format(self)     



class Document(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True) 
    def __str__(self):
        return self.name 

class Project(models.Model):
    title = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    members = models.ManyToManyField(User, through='Isconfirmed')
    documents = models.ManyToManyField(Document, through='Doclocation')

    def __str__(self):
            template = '{0.title} {0.description} {0.created} {0.updated}'
            return template.format(self)

class Isconfirmed(models.Model):
    status = models.BooleanField(default=False,null=True, blank=True)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True) 
         

class Doclocation(models.Model):
    filelocation = models.FileField(null=True, blank=True)
    approved = models.BooleanField(default=None,null=True, blank=True)
    reviews = models.TextField(null=True, blank=True)  
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
            template = '{0.filelocation}'
            return template.format(self)



class Meeting(models.Model):
    description = models.TextField(null=True, blank=True)
    deadline =  models.DateField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        template = '{0.description} {0.deadline}'
        return template.format(self)            







class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
        role_id = models.ForeignKey(Role, on_delete=models.DO_NOTHING,null=True, blank=True)
        designation_id = models.ForeignKey(Designation, on_delete=models.DO_NOTHING,null=True, blank=True)
        semester=models.IntegerField(null=True, blank=True)

        def __str__(self):
            template = '{0.role_id} {0.semester}'
            return template.format(self)


        