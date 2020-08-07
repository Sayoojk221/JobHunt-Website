from django.http import HttpResponse
from django.shortcuts import redirect,render

def unauthenticated(view_fun):
    def check_user(request):
        if request.session.has_key('employer-id'):
            return redirect('/employerhome/')
        elif request.session.has_key('employee-id'):
            return redirect('/employeehome/')
        else:
            return view_fun(request)
    return check_user


def unauthenticated_employee(view_func):
    def check_employee(request):
        if request.session.has_key('employee-id'):
            return view_func(request)
        else:
            if request.session.has_key('employer-id'):
                return redirect('/employerhome/')
            else:
                return render(request,'login&register/login.html',{'error':'Login Please'})
    return check_employee

def unauthenticated_employer(view_func):
    def check_employer(request):
        if request.session.has_key('employer-id'):
            return view_func(request)
        else:
            if request.session.has_key('employee-id'):
                return redirect('/employeehome/')
            else:
                return render(request,'login&register/login.html',{'error':'Login Please'})
    return check_employer

