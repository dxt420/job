from django.contrib import admin
from django.contrib.auth import get_user_model


# Register your models here.
from .models import *

from django.db import models

# Create your models here.


admin.site.register(CVPri)
admin.site.register(Job)
admin.site.register(Company)
admin.site.register(CustomUser)
admin.site.register(CVEdu)
admin.site.register(CVLan)
admin.site.register(Seeker)
admin.site.register(CVWork)
admin.site.register(AppliedJobs)
# admin.site.register(CVEdu)

# class CVPri(models.Model):


# class CVEdu(models.Model):

# class CVWork(models.Model):

# class CVPro(models.Model):


# class Company(models.Model):


# class Job(models.Model):


