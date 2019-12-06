from django.contrib import admin

# Register your models here.
from login.models import UserProfile
from login.models import Project
from .models import Meeting
from .models import Document
from .models import Role
from .models import Designation
from .models import Doclocation
from .models import Isconfirmed
from .models import Calendar

admin.site.register(Project)
admin.site.register(Meeting)
admin.site.register(Designation)
admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(Role)
admin.site.register(Doclocation)
admin.site.register(Isconfirmed)
admin.site.register(Calendar)