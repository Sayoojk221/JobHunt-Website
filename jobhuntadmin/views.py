from django.shortcuts import render,HttpResponse
from .models import *
from emp.models import *
from jobportal import settings
import random
from django.core.mail import send_mail
from .decorator import *
import datetime

@twofactorauthencation
def authencation(request):
    adminemail = AdminLogin.objects.get(id=1)
    check = TwoFactorAuthentication.objects.all()

    if request.method == 'POST':
        authentication_details = TwoFactorAuthentication.objects.get(id=1)
        code = request.POST['code']
        if code == str(authentication_details.code):
            TwoFactorAuthentication.objects.all().filter(id=1).update(status='success')
            return render(request,'admin/adminlogin.html')
        else:
            return render(request,'admin/authencation.html',{'message':'Code Incorrect'})

    else:
        if check:
            pass
        else:
            value = TwoFactorAuthentication(code='0000',status='failed')
            value.save()

        digit = random.randint(1000,9999)
        subject = 'Two-Factor Authentication'
        message = f'Your code : {digit}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [adminemail.email]
        send_mail(subject, message, email_from, recipient_list,fail_silently=False)
        TwoFactorAuthentication.objects.all().filter(id=1).update(code=digit)
        return render(request,'admin/authencation.html',{'message':'Authentication code sent to registered Email'})

@admin
def loginadmin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        admin_details = AdminLogin.objects.all().filter(email=email,password=password)
        if admin_details:
            for item in admin_details:
                request.session['admin-id']=item.id
            return redirect('/admin/home/')
        else:
            return render(request,'admin/adminlogin.html',{'message':'Invalid email and password'})
    else:
        return render(request,'admin/adminlogin.html')

@adminlogincheck
def home(request):
    return render(request,'admin/home.html')

def logout(request):
    TwoFactorAuthentication.objects.all().filter(id=1).update(status='failed')
    del request.session['admin-id']
    return redirect('/')

@adminlogincheck
def employees(request):
    personal = EmployeePersonalDetails.objects.all()
    context = {'employee_per':personal}
    return render(request,'admin/totalemployee.html',context)

@adminlogincheck
def employers(request):
    employers = EmployerRegister.objects.all()
    context = {'employers':employers}
    return render(request,'admin/totalemployer.html',context)

@adminlogincheck
def single_employee(request):
    employeeid = request.GET.get('id')
    employee_dob = EmployeePersonalDetails.objects.all().filter(employeeid=employeeid).values_list('age')
    value = [i for j in employee_dob for i in j]
    dob = str(value[0])
    employee_age = datetime.date.today().year - int(dob[:4])
    job = EmployeeJobDetails.objects.all().filter(employeeid=employeeid)
    social = EmployeeSocialDetails.objects.all().filter(employeeid=employeeid)
    personal = EmployeePersonalDetails.objects.all().filter(employeeid=employeeid)
    education = EmployeeEducation.objects.all().filter(employeeid=employeeid)
    personalresume = EmployeePersonalResume.objects.all().filter(employeeid=employeeid)
    workexperience = EmployeeWorkExperience.objects.all().filter(employeeid=employeeid)
    portflio = EmployeePortfolio.objects.all().filter(employeeid=employeeid)
    professionalskill = EmployeeProfessionalSkill.objects.all().filter(employeeid=employeeid)
    languageskill = EmployeeLanguageSkill.objects.all().filter(employeeid=employeeid)
    awards = EmployeeAwards.objects.all().filter(employeeid=employeeid)
    context = {'resume':personalresume,'age':employee_age,'employee_per':personal,'education':education,'workexperience':workexperience,'portflio':portflio,'professionalskill':professionalskill,'languageskill':languageskill,'awards':awards,'employee_job':job,'employee_social':social}
    return render(request,'admin/singleemployee.html',context)

@adminlogincheck
def single_employer(request):
    employerid = request.GET.get('id')
    employersocial = EmployerSocialDetails.objects.all().filter(employerid=employerid)
    postedjobcount = EmployerNewJobPost.objects.all().filter(employerid=employerid).count()
    postedjobs = EmployerNewJobPost.objects.all().filter(employerid=employerid)
    employer_details = EmployerRegister.objects.all().filter(id=employerid)
    context = {'employersocial':employersocial,'postedjobs':postedjobs,'count':postedjobcount,'employer':employer_details}
    return render(request,'admin/singleemployer.html',context)
@adminlogincheck
def active_log(request):
    details = JobApplication.objects.all()
    context = {'jobrequest':details}
    return render(request,'admin/activelog.html',context)
