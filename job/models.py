from django.db import models
from .choices import *
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

class CustomUser(AbstractUser):
    is_company = models.BooleanField(default="False")
    is_seeker = models.BooleanField(default="False")



class CVPri(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,primary_key=True)
    full_name = models.CharField(max_length=100)
    age = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class CVEdu(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank="True")
    title = models.CharField(max_length=100)
    from_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    school = models.CharField(max_length=100,blank="True")
    level = models.CharField(max_length=100,blank="True")
    
    def __str__(self):
        return self.title

class CVWork(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank="True")
    title = models.CharField(max_length=100)
    from_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    companytype = models.CharField(max_length=100,blank="True")
    description = models.CharField(max_length=500,blank="True")
    
    def __str__(self):
        return self.title

class CVPro(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank="True")
    title = models.CharField(max_length=100)
    percent = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class CVLan(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank="True")
    title = models.CharField(max_length=100)
    spoken = models.CharField(max_length=100)
    written = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class CVRef(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank="True")
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


# to be user ************************ employer user***************************************
class Company(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    title = models.CharField(max_length=100)
    since = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    logo = models.ImageField(upload_to="media/company",blank="True")
 
    def __str__(self):
        return self.title
    
    def open_positions(self):
        return Job.objects.filter(company=self,status=True).count()

    def posted_jobs(self):
        return Job.objects.filter(company=self).count()

class Seeker(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100,blank="True")
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100,blank="True")
    address = models.CharField(max_length=100,blank="True")
    description = models.CharField(max_length=500,blank="True")
    usericon = models.ImageField(upload_to="media/seekersicon",blank="True") 
    rating = models.IntegerField(blank=True,default=0)
 
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        ordering=['-rating']




class Job(models.Model):
    title = models.CharField(max_length=100)
    jobtype = models.CharField(max_length=100)
    # jobtype = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,blank="True")
    phone = models.CharField(max_length=100,blank="True")
    email = models.CharField(max_length=100,blank="True")
    offered_salary = models.CharField(max_length=100)
    exp = models.CharField(max_length=100)
    jobindustry =models.CharField(max_length=100)
    deadline = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    skills2 = models.CharField(max_length=1000,blank="True")
    exp2 = models.CharField(max_length=1000,blank="True")
    gender =  models.CharField(max_length=100,blank="True")
    status =  models.BooleanField(default="True",blank="True")
    date_created =  models.DateTimeField(auto_now="True")
    people = models.IntegerField(blank=True,default=0)
    
    

    company =  models.ForeignKey("Company", on_delete=models.CASCADE) 
    def __str__(self):
        return self.title

    def appliedcount(self):
        return AppliedJobs.objects.filter(job=self).count()




class AppliedJobs(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    seeker = models.ForeignKey(Seeker,on_delete=models.CASCADE)
    cover = models.FileField(upload_to="media/files/cover",blank="True") 
    academic = models.FileField(upload_to="media/files/academic",blank="True") 
    rec = models.FileField(upload_to="media/files/recomendations",blank="True")
    date_applied=  models.DateTimeField(auto_now="True")
    academic_extract = models.CharField(max_length=5000,blank="True")
    status =  models.BooleanField(default="False",blank="True")
    limit_reached =  models.BooleanField(default="False",blank="True")
 

    def userr(self):
        return self.seeker.user

    class Meta:
        ordering=['-seeker__rating']


class Extract(models.Model):
    seeker = models.ForeignKey(Seeker,on_delete=models.CASCADE)
    result = models.CharField(max_length=500)

   





