from django.db import models

class AdminLogin(models.Model):
    email = models.CharField(max_length=200,default='')
    password = models.CharField(max_length=200,default='')

class TwoFactorAuthentication(models.Model):
    code = models.CharField(max_length=200,default='')
    status = models.CharField(max_length=200,default='')
