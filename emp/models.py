from django.db import models
from django.utils.timezone import now
# -*- coding: utf-8 -*-
# Create your models here.

class EmployerRegister(models.Model):
    logo = models.ImageField(upload_to='employerlogo',null='empty')
    companyname = models.CharField(max_length=200,null='empty')
    companyemail = models.CharField(max_length=200,null='empty')
    password = models.CharField(max_length=50,null='empty')
    phoneno = models.CharField(max_length=200,null='empty')
    country = models.CharField(max_length=200,null='empty')
    address = models.CharField(max_length=500,null='empty')
    city = models.CharField(max_length=200,null='empty')
    state = models.CharField(max_length=200,null='empty')
    since = models.CharField(max_length=200,null='empty')
    teamsize = models.CharField(max_length=200,null='empty')
    category = models.CharField(max_length=200,null='empty')
    description = models.CharField(max_length=2000,null='empty')
    website = models.CharField(max_length=200,null='empty')
    authentication = models.CharField(max_length=200,default='')

class EmployerSocialDetails(models.Model):
    employerid = models.ForeignKey(EmployerRegister,on_delete=models.CASCADE)
    facebook = models.URLField(max_length=200,default='')
    twitter = models.URLField(max_length=200,default='')
    linkedin = models.URLField(max_length=200,default='')
    google = models.URLField(max_length=200,default='')

class EmployeeRegister(models.Model):
    profileimage = models.ImageField(upload_to='employeeimage',null='empty')
    username = models.CharField(max_length=200,null='empty')
    password = models.CharField(max_length=200,null='empty')
    email = models.CharField(max_length=200,null='empty')
    phoneno = models.CharField(max_length=200,null='empty')
    authentication = models.CharField(max_length=200,default='')

class EmployeePersonalDetails(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200,null='empty')
    age = models.CharField(max_length=200,null='empty')
    education = models.CharField(max_length=200,null='empty')
    country = models.CharField(max_length=200,null='empty')
    address = models.CharField(max_length=700,null='empty')
    state = models.CharField(max_length=200,null='empty')
    city = models.CharField(max_length=200,null='empty')
    gender = models.CharField(max_length=200,null='empty')
    description = models.CharField(max_length=10000,null='empty')

class EmployeeJobDetails(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    company = models.CharField(max_length=200,null='empty')
    jobtitle = models.CharField(max_length=200,null='empty')
    experience = models.CharField(max_length=200,null='empty')
    currentsalary = models.CharField(max_length=200,null='empty')

class EmployeeSocialDetails(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    facebook = models.URLField(max_length=200,null='empty')
    linkedin = models.URLField(max_length=200,null='empty')
    twitter = models.URLField(max_length=200,null='empty')

class EmployerNewJobPost(models.Model):
    employerid = models.ForeignKey(EmployerRegister,on_delete=models.CASCADE)
    jobcode = models.CharField(max_length=200,null='empty')
    jobtitle = models.CharField(max_length=200,null='empty')
    description = models.CharField(max_length=2000,null='empty')
    email = models.CharField(max_length=200,null='empty')
    jobtype = models.CharField(max_length=200,null='empty')
    offerdsalary = models.CharField(max_length=200,null='empty')
    careerlevel = models.CharField(max_length=200,null='empty')
    experience = models.CharField(max_length=200,null='empty')
    qualification = models.CharField(max_length=200,null='empty')
    gender = models.CharField(max_length=200,null='empty')
    industry = models.CharField(max_length=200,null='empty')
    country = models.CharField(max_length=200,null='empty')
    city = models.CharField(max_length=200,null='empty')
    deadline = models.CharField(max_length=200,null='empty')
    createddate = models.DateTimeField(default=now())
    requiredknowledge = models.CharField(max_length=2000,null='empty')
    educationandexperience = models.CharField(max_length=2000,null='empty')
    positionnumber =  models.CharField(max_length=200,null='empty')
    linkedinurl = models.URLField(max_length=200,null='empty')
    status = models.CharField(max_length=200,null='empty')

class EmployeeEducation(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null='empty')
    course = models.CharField(max_length=200,null='empty')
    institute = models.CharField(max_length=200,null='empty')
    startyear= models.CharField(max_length=200,null='empty')
    endyear = models.CharField(max_length=200,null='empty')
    description = models.CharField(max_length=500,null='empty')

class EmployeeWorkExperience(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    job = models.CharField(max_length=200,null='empty')
    company = models.CharField(max_length=200,null='empty')
    startyear = models.CharField(max_length=200,null='empty')
    endyear = models.CharField(max_length=200,null='empty')
    jobdescription = models.CharField(max_length=500,null='empty')
    present_status = models.CharField(max_length=200,null='empty')

class EmployeePortfolio(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    url = models.URLField(max_length=200,null='empty')
    image = models.ImageField(upload_to='portfolio',null='empty')

class EmployeeProfessionalSkill(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    skillname = models.CharField(max_length=200,null='empty')
    percentage = models.PositiveIntegerField(null='empty')

class EmployeeLanguageSkill(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    language = models.CharField(max_length=200,null='empty')
    percentage = models.PositiveIntegerField(null='empty')

class EmployeeAwards(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    awardname = models.CharField(max_length=200,null='empty')
    year = models.CharField(max_length=200,null='empty')
    description = models.CharField(max_length=500,null='empty')

class CandidatesList(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    employeepersonalid = models.ForeignKey(EmployeePersonalDetails,on_delete=models.CASCADE)
    employeejobdetailsid  = models.ForeignKey(EmployeeJobDetails,on_delete=models.CASCADE)
    status = models.CharField(max_length=200,null='empty')


class JobApplication(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    employeepersonalid = models.ForeignKey(EmployeePersonalDetails,on_delete=models.CASCADE,default='')
    employeejobdetails = models.ForeignKey(EmployeeJobDetails,on_delete=models.CASCADE,default='')
    jobid = models.ForeignKey(EmployerNewJobPost,on_delete=models.CASCADE)
    date = models.DateTimeField(default=now())
    interviewdate = models.CharField(max_length=200,default='')
    lettersenddate = models.CharField(max_length=200,default='')
    acceptdate = models.CharField(max_length=200,default='')
    rejectdate = models.CharField(max_length=200,default='')
    status = models.CharField(max_length=200,default='')

class JobShortlists(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    shortlistedjobid = models.ForeignKey(EmployerNewJobPost,on_delete=models.CASCADE)
    date = models.DateTimeField(default=now())
    status = models.CharField(max_length=200,default='')

class EmployeeCoverLetter(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    description = models.CharField(max_length=2000,default='')

class EmployeeProfileShortlists(models.Model):
    employerid = models.ForeignKey(EmployerRegister,on_delete=models.CASCADE)
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    employeepersonalid = models.ForeignKey(EmployeePersonalDetails,on_delete=models.CASCADE,default='')
    employeejobid = models.ForeignKey(EmployeeJobDetails,on_delete=models.CASCADE,default='')
    date = models.DateTimeField(default=now())
    interviewdate = models.CharField(max_length=200,default='')
    lettersenddate = models.CharField(max_length=200,default='')
    acceptdate = models.CharField(max_length=200,default='')
    rejectdate = models.CharField(max_length=200,default='')
    status = models.CharField(max_length=200,default='')

class deletedcandidates(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    employerid = models.ForeignKey(EmployerRegister,on_delete=models.CASCADE)

class EmployeeReview(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    employeepersonalid = models.ForeignKey(EmployeePersonalDetails,on_delete=models.CASCADE)
    review = models.CharField(max_length=1000,default='')

class EmployeePersonalResume(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='personalresume',null='empty')
