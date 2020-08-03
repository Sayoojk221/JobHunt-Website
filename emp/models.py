from django.db import models
import datetime
# -*- coding: utf-8 -*-
# Create your models here.

class EmployerRegister(models.Model):
    logo = models.ImageField(upload_to='employerlogo',null='Empty')
    companyname = models.CharField(max_length=200,null='Empty')
    companyemail = models.CharField(max_length=200,null='Empty')
    password = models.CharField(max_length=50,null='Empty')
    phoneno = models.CharField(max_length=200,null='Empty')
    country = models.CharField(max_length=200,null='Empty')
    state = models.CharField(max_length=200,null='Empty')
    since = models.CharField(max_length=200,null='Empty')
    teamsize = models.CharField(max_length=200,null='Empty')
    category = models.CharField(max_length=200,null='Empty')
    description = models.CharField(max_length=2000,null='Empty')
    website = models.CharField(max_length=200,null='Empty')
    authentication = models.CharField(max_length=200,default='')

class EmployerSocialDetails(models.Model):
    employerid = models.ForeignKey(EmployerRegister,on_delete=models.CASCADE)
    facebook = models.CharField(max_length=200,null='Empty')
    twitter = models.CharField(max_length=200,null='Empty')
    linkedin = models.CharField(max_length=200,null='Empty')
    google = models.CharField(max_length=200,null='Empty')

class EmployeeRegister(models.Model):
    profileimage = models.ImageField(upload_to='employeeimage',null='Empty')
    username = models.CharField(max_length=200,null='Empty')
    password = models.CharField(max_length=200,null='Empty')
    email = models.CharField(max_length=200,null='Empty')
    phoneno = models.CharField(max_length=200,null='Empty')
    authentication = models.CharField(max_length=200,default='')

class EmployeePersonalDetails(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200,null='Empty')
    age = models.CharField(max_length=200,null='Empty')
    education = models.CharField(max_length=200,null='Empty')
    country = models.CharField(max_length=200,null='Empty')
    city = models.CharField(max_length=200,null='Empty')


class EmployeeJobDetails(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    jobtitle = models.CharField(max_length=200,null='Empty')
    experience = models.CharField(max_length=200,null='Empty')
    currentsalary = models.CharField(max_length=200,null='Empty')
    jobdescription = models.CharField(max_length=1000,null='Empty')

class EmployeeSocialDetails(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    facebook = models.CharField(max_length=200,null='Empty')
    linkedin = models.CharField(max_length=200,null='Empty')
    twitter = models.CharField(max_length=200,null='Empty')

class EmployerNewJobPost(models.Model):
    employerid = models.ForeignKey(EmployerRegister,on_delete=models.CASCADE)
    jobtitle = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=2000,null=True)
    email = models.CharField(max_length=200,null=True)
    jobtype = models.CharField(max_length=200,null=True)
    offerdsalary = models.CharField(max_length=200,null=True)
    careerlevel = models.CharField(max_length=200,null=True)
    experience = models.CharField(max_length=200,null=True)
    gender = models.CharField(max_length=200,null=True)
    industry = models.CharField(max_length=200,null=True)
    qualification = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    deadline = models.CharField(max_length=200,null=True)
    createddate = models.DateTimeField(default=datetime.date.today())
    requiredknowledge = models.CharField(max_length=2000,null=True)
    educationandexperience = models.CharField(max_length=2000,null=True)

class EmployeeEducation(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True)
    course = models.CharField(max_length=200,null=True)
    institute = models.CharField(max_length=200,null=True)
    fromdate = models.CharField(max_length=200,null=True)
    todate = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=500,null=True)

class EmployeeWorkExperience(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    job = models.CharField(max_length=200,null=True)
    company = models.CharField(max_length=200,null=True)
    fromdate = models.CharField(max_length=200,null=True)
    todate = models.CharField(max_length=200,null=True)
    jobdescription = models.CharField(max_length=500,null=True)
    present_status = models.CharField(max_length=200,null=True)

class EmployeePortfolio(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True)
    image = models.ImageField(upload_to='portfolio',null=True)

class EmployeeProfessionalSkill(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    skillname = models.CharField(max_length=200,null=True)
    percentage = models.PositiveIntegerField(null=True)

class EmployeeLanguageSkill(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    language = models.CharField(max_length=200,null=True)
    percentage = models.PositiveIntegerField(null=True)

class EmployeeAwards(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True)
    fromdate = models.CharField(max_length=200,null=True)
    todate = models.CharField(max_length=200,null=True)


