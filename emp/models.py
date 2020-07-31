from django.db import models

# -*- coding: utf-8 -*-
# Create your models here.

class EmployerRegister(models.Model):
    companyname = models.CharField(max_length=200,null='True')
    companyemail = models.CharField(max_length=200,null='True')
    password = models.CharField(max_length=50,null='True')
    phoneno = models.CharField(max_length=200,null='True')
    country = models.CharField(max_length=200,null='True')
    state = models.CharField(max_length=200,null='True')
    city = models.CharField(max_length=200,null='True')
    authentication = models.CharField(max_length=200,default='')
class EmployerDetails(models.Model):
    logo = models.ImageField(upload_to='employerlogo',null='True')
    employerid = models.ForeignKey(EmployerRegister,on_delete=models.CASCADE)
    since = models.CharField(max_length=200,null='True')
    teamsize = models.CharField(max_length=200,null='True')
    category = models.CharField(max_length=200,null='True')
    description = models.CharField(max_length=2000,null='True')

class EmployerSocialDetails(models.Model):
    employerid = models.ForeignKey(EmployerRegister,on_delete=models.CASCADE)
    facebook = models.CharField(max_length=200,null='True')
    twitter = models.CharField(max_length=200,null='True')
    linkedin = models.CharField(max_length=200,null='True')
    google = models.CharField(max_length=200,null='True')

class EmployeeRegister(models.Model):
    username = models.CharField(max_length=200,null='True')
    password = models.CharField(max_length=200,null='True')
    email = models.CharField(max_length=200,null='True')
    phoneno = models.CharField(max_length=200,null='True')
    authentication = models.CharField(max_length=200,default='')

class EmployeePersonalDetails(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    profileimage = models.ImageField(upload_to='employeeimage',null='True')
    fullname = models.CharField(max_length=200,null='True')
    age = models.CharField(max_length=200,null='True')
    education = models.CharField(max_length=200,null='True')
    lanquages = models.CharField(max_length=200,null='True')
    country = models.CharField(max_length=200,null='True')
    state = models.CharField(max_length=200,null='True')
    city = models.CharField(max_length=200,null='True')


class EmployeeJobDetails(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    jobtitle = models.CharField(max_length=200,null='True')
    experience = models.CharField(max_length=200,null='True')
    currentsalary = models.CharField(max_length=200,null='True')
    currentsalarymax = models.CharField(max_length=200,null='True')
    expectedsalary = models.CharField(max_length=200,null='True')
    expectedsalarymax = models.CharField(max_length=200,null='True')
    jobdescription = models.CharField(max_length=1000,null='True')

class EmployeeSocialDetails(models.Model):
    employeeid = models.ForeignKey(EmployeeRegister,on_delete=models.CASCADE)
    linkedin = models.CharField(max_length=200,null='True')
    twitter = models.CharField(max_length=200,null='True')



