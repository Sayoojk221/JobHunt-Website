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
		usertype = request.POST['select']
		employer_existcheck = EmployerRegister.objects.all().filter(companyemail=email).count()
		employee_existcheck = EmployeeRegister.objects.all().filter(email=email).count()
		if usertype == 'Employer' and employer_existcheck == 0:
			subject = 'welcome to Job Hunt IT Solution'
			message = f'Hi {name}, thank you for registering in Job Hunt IT Solution. your  Company email: {email} and  password: {password}.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email, ]
			send_mail( subject, message, email_from, recipient_list)
			employer_details = EmployerRegister(logo='/images/employerlogo/default.jpg',companyname=name,companyemail=email,password=password,phoneno=phone,authentication='pending')
			employer_details.save()
			employer_existcheck = 0
			return render(request,'login&register/login.html',{'success':"Successfully registered"})
		elif usertype == 'Candidate' and employee_existcheck == 0:
			subject = 'welcome to Leaders IT Solution'
			message = f'Hi {name}, thank you for registering in Job Hunt IT Solution. your  email: {email} and  password: {password}.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email, ]
			send_mail(subject, message, email_from, recipient_list)
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
	employer_details = EmployerRegister.objects.all().filter(id=employerid)
	context = {'employer_reg':employer_details}
	return render(request,'employer/employerhome.html',context)


def employer_profile(request):
	employer = request.session['employer-id']
	if request.method == 'POST':
		logo = request.FILES.get('logo')
		name = request.POST['companyname']
		category = request.POST['category']
		since = request.POST['since']
		teamsize = request.POST['teamsize']
		description = request.POST['description']
		employerid.logo = logo
		employerid.save()
		EmployerRegister.objects.all().filter(id=employer).update(companyname=name,category=category,since=since,teamsize=teamsize,description=description)
		current_employer = EmployerRegister.objects.all().filter(id=employer)
		context = {'employer_reg':current_employer}
		return render(request,'employer/profile.html',context)
	else:
		current_employer = EmployerRegister.objects.all().filter(id=employer)
		current_employer_socialdetails = EmployerSocialDetails.objects.filter(employerid=employer)
		if current_employer_socialdetails:
			context = {'employer_reg':current_employer,'employer_social':current_employer_socialdetails}
			return render(request,'employer/profile.html',context)
		else:
			context = {'employer_reg':current_employer}
			return render(request,'employer/profile.html',context)

def employer_contactdetails(request):
	employer = request.session['employer-id']
	if request.method == 'POST':
		website = request.POST['website']
		country = request.POST['country']
		state = request.POST['state']
		EmployerRegister.objects.all().filter(id=employer).update(website=website,country=country,state=state)
		return redirect('/employerprofile/')
	else:
		return redirect('/employerprofile/')

def employer_socialnetworksdetails(request):
	employer = request.session['employer-id']
	employerid = EmployerRegister.objects.get(id=employer)
	employer_exist = EmployerSocialDetails.objects.all().filter(employerid=employer).values('employerid')
	empid = 0
	for item in employer_exist:
		for i in item:
				empid = i
	if empid == 0:
		if request.method == 'POST':
			facebook = request.POST['facebook']
			twitter = request.POST['twitter']
			google = request.POST['google']
			linkedin = request.POST['linkedin']
			social_details = EmployerSocialDetails(employerid=employerid,facebook=facebook,twitter=twitter,google=google,linkedin=linkedin)
			social_details.save()
			return redirect('/employerprofile/')
		else:
			return redirect('/employerprofile/')
	else:
		if request.method == 'POST':
			facebook = request.POST['facebook']
			twitter = request.POST['twitter']
			google = request.POST['google']
			linkedin = request.POST['linkedin']
			EmployerSocialDetails.objects.all().filter(employerid=employerid).update(facebook=facebook,twitter=twitter,google=google,linkedin=linkedin)
			return redirect('/employerprofile/')
		else:
			return redirect('/employerprofile/')



