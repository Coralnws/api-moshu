from importlib import import_module
from django.contrib import admin
from .models.users import CustomUser
from .models.teams import Team
from .models.projects import Project
from .models.documents import Document
from .models.invitations import Invitation
from .models.userRelations import *

# Register your models here.

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

class TeamAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'teamName', 'createdBy','createdAt')

class ProjectAdminConfig(admin.ModelAdmin):
    list_display = ('id','title','belongTo')

class DocumentAdminConfig(admin.ModelAdmin):
    list_display = ('id','title','belongTo')

class InvitationAdminConfig(admin.ModelAdmin):
    list_display = ('id','user','team','result')

class UserTeamAdminConfig(admin.ModelAdmin):
    list_display = ('team', 'user', 'isAdmin', 'isMainAdmin')

class UserProjectAdminConfig(admin.ModelAdmin):
    list_display = ('project', 'user', 'isAdmin', 'isMainAdmin')



admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Team, TeamAdminConfig)
admin.site.register(Project, ProjectAdminConfig)
admin.site.register(Document, DocumentAdminConfig)
admin.site.register(Invitation, InvitationAdminConfig)
admin.site.register(UserTeam, UserTeamAdminConfig)
admin.site.register(UserProject, UserProjectAdminConfig)