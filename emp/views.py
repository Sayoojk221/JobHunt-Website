from django.shortcuts import render,redirect
from jobportal import settings
from emp.models import *
from django.core.mail import send_mail

# Create your views here.

def home(request):

	return render(request,'home/home.html')

def register_both(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['pass']
		phone = request.POST['phone']
		usertype = request.POST.get('usertype')
		employer_existcheck = EmployerRegister.objects.all().filter(companyemail=email).count()
		employee_existcheck = EmployeeRegister.objects.all().filter(email=email).count()

		if usertype == 'Employer' and employer_existcheck == 0:
			subject = 'welcome to Leaders IT Solution'
			message = f'Hi {name}, thank you for registering in leaders it solution. your  Company email: {email} and  password: {password}.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email, ]
			send_mail( subject, message, email_from, recipient_list, fail_silently=False)
			employer_details = EmployerRegister(companyname=name,companyemail=email,password=password,phoneno=phone,authentication='pending')
			employer_details.save()
			employer_existcheck = 0
			return render(request,'login&register/login.html',{'success':"Successfully registered"})
		elif usertype == 'Candidate' and employee_existcheck == 0:
			subject = 'welcome to Leaders IT Solution'
			message = f'Hi {name}, thank you for registering in leaders it solution. your  email: {email} and  password: {password}.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email, ]
			send_mail(subject, message, email_from, recipient_list )
			employee_details = EmployeeRegister(username=name,password=password,email=email,phoneno=phone,authentication='pending')
			employee_details.save()
			employee_existcheck = 0
			return render(request,'login&register/login.html',{'success':"Successfully registered"})
		else:
			if employer_existcheck > 0:
				return render(request,'login&register/register.html',{'error':name+" employer already registered "})
			elif employee_existcheck > 0:
				return render(request,'login&register/register.html',{'error':name+" employee already registered "})
	else:
	 	return render(request,'login&register/register.html')

def login_both(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['pass']
		usertype = request.POST.get('usertype')
		employer_existcheck = EmployerRegister.objects.all().filter(companyemail=email,password=password).count()
		employee_existcheck = EmployeeRegister.objects.all().filter(email=email,password=password).count()

		if usertype == 'Employer' and employer_existcheck == 1:
			employer_existcheck = 0
			employer_details = EmployerRegister.objects.all().filter(companyemail=email,authentication='success')
			for item in employer_details:
				request.session['employer-id']=item.id
			if employer_details:
				return redirect('/employerhome/')
			else:
				return render(request,'login&register/login.html',{'error':'Please check '+email+' for activate account'})
		elif usertype == 'Candidate' and employee_existcheck == 1:
			employee_existcheck = 0
			employee_details = EmployeeRegister.objects.all().filter(email=email,authentication='success')
			for item in employee_details:
				request.session['employee-id']=item.id
			if employee_details:
				return render(request,'employee/employeehome.html')
			else:
				return render(request,'login&register/login.html',{'error':'Please check '+email+' for activate account'})
		else:
			return render(request,'login&register/login.html',{'error':email+' not registered '})


	else:
		return render(request,'login&register/login.html')

def employer_logout(request):
	if request.session.has_key('employer-id'):
		del request.session['employer-id']
		return redirect('/')

def employer_home(request):
	employerid = request.session['employer-id']
	print(employerid)
	employer_details = EmployerRegister.objects.all().filter(id=employerid)
	print(employer_details)
	context = {'employer':employer_details}
	return render(request,'employer/employerhome.html',context)

