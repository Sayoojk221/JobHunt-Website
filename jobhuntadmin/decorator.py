from django.http import HttpResponse
from django.shortcuts import redirect,render
from .models import TwoFactorAuthentication

def twofactorauthencation(data_func):
    def check(request):
        if request.session.has_key('admin-id'):
            return redirect('/admin/home/')
        else:
            return data_func(request)
    return check

def admin(data_func):
    def check(request):
        auth_detail = TwoFactorAuthentication.objects.get(id=1)
        if request.session.has_key('admin-id'):
            return redirect('/admin/home/')
        else:
            if auth_detail.status == 'failed':
                return redirect('/admin/')
            else:
                return data_func(request)
    return check

def adminlogincheck(data_func):
    def check(request):
        if request.session.has_key('admin-id'):
            return data_func(request)
        else:
            return redirect('/admin/login/')
    return check
