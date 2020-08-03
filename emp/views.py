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
			employee_details = EmployeeRegister(profileimage='/images/employeeimage/default.jpg',username=name,password=password,email=email,phoneno=phone,authentication='pending')
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
				employeeid = item.id
			if employee_details:
				employeeid_exist = EmployeePersonalDetails.objects.all().filter(employeeid=employeeid).values('employeeid')
				exist_value = 0
				for item in employeeid_exist:
					for i in item:
							exist_value = i
				if exist_value == 0:
					employee_foriegn_data = EmployeeRegister.objects.get(id=employeeid)
					personaldetails = EmployeePersonalDetails(employeeid=employee_foriegn_data)  #creating the database for storing
					jobdetails = EmployeeJobDetails(employeeid=employee_foriegn_data)			 #employee personal,job,social details
					socialdetails = EmployeeSocialDetails(employeeid=employee_foriegn_data)
					personaldetails.save()
					jobdetails.save()
					socialdetails.save()
					return redirect('/employeehome/')
				else:
					return redirect('/employeehome/')
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
		if logo:
			employer_details = EmployerRegister.objects.get(id=employer)
			employer_details.logo = logo
			employer_details.save()
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


def postnew_job(request):
	employer = request.session['employer-id']
	if request.method == 'POST':
		employerid = EmployerRegister.objects.get(id=employer)
		jobtitle = request.POST['title']
		description = request.POST['descr']
		email = request.POST['email']
		jobtype = request.POST['jobtype']
		salary = request.POST['salary']
		level = request.POST['careerlevel']
		experience = request.POST['experience']
		gender = request.POST['gender']
		industry = request.POST['industry']
		qualification = request.POST.get('qualification')
		country = request.POST['country']
		city = request.POST['city']
		deadline = request.POST['deadline']
		knowledge = request.POST['requiredknowledge']
		educationandexperience = request.POST['edu+exp']
		job_detais = EmployerNewJobPost(employerid=employerid,jobtitle=jobtitle,description=description,email=email,jobtype=jobtype,offerdsalary=salary,careerlevel=level,experience=experience,gender=gender,industry=industry,qualification=qualification,country=country,city=city,deadline=deadline,requiredknowledge=knowledge,educationandexperience=educationandexperience)
		job_detais.save()
		return redirect('/postnewjob/')
	else:
		current_employer =EmployerRegister.objects.all().filter(id=employer)
		context = {'employer_reg':current_employer}
		return render(request,'employer/postnewjob.html',context)


def employee_home(request):
	employee = request.session['employee-id']
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	context = {'employee_reg':current_employee}
	return render(request,'employee/employeehome.html',context)

def employee_profile(request):
	employee = request.session['employee-id']
	if request.method == 'POST':
		profilepic = request.FILES.get('image')
		fullname = request.POST['fullname']
		jobtitle = request.POST['jobtitle']
		salary = request.POST['salary']
		experience = request.POST['exp']
		education = request.POST['edu']
		age = request.POST['age']
		description = request.POST['desc']

		if profilepic:
			employee_details = EmployeeRegister.objects.get(id=employee)
			employee_details.profileimage = profilepic
			employee_details.save()

		EmployeePersonalDetails.objects.all().filter(employeeid=employee).update(fullname=fullname,age=age,education=education)
		EmployeeJobDetails.objects.all().filter(employeeid=employee).update(jobtitle=jobtitle,experience=experience,currentsalary=salary,jobdescription=description)
		return redirect('/employeeprofile/')

	else:
		current_employee = EmployeeRegister.objects.all().filter(id=employee)
		current_employee_personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
		current_employee_job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
		current_employee_social = EmployeeSocialDetails.objects.all().filter(employeeid=employee)
		context = {'employee_reg':current_employee,'employee_per':current_employee_personal,'employee_job':current_employee_job,'employee_social':current_employee_social}
		return render(request,'employee/profile.html',context)


def employeesocial_networks(request):
	employee = request.session['employee-id']
	if request.method == 'POST':
		facebook = request.POST['facebook']
		linkedin = request.POST['linkedin']
		twitter = request.POST['twitter']

		EmployeeSocialDetails.objects.all().filter(id=employee).update(facebook=facebook,linkedin=linkedin,twitter=twitter)
		return redirect('/employeeprofile/')
	else:
		return redirect('/employeeprofile/')

def employee_contact(request):
	employee = request.session['employee-id']
	if request.method == 'POST':
		phone = request.POST['phone']
		email = request.POST['email']
		country = request.POST['country']
		city = request.POST['city']

		EmployeeRegister.objects.all().filter(id=employee).update(phoneno=phone,email=email)
		EmployeePersonalDetails.objects.all().filter(employeeid=employee).update(country=country,city=city)
		return redirect('/employeeprofile/')
	else:
		return redirect('/employeeprofile/')


def employee_resume(request):
	employee = request.session['employee-id']
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	education = EmployeeEducation.objects.all().filter(employeeid=employee)
	workexperience = EmployeeWorkExperience.objects.all().filter(employeeid=employee)
	portflio = EmployeePortfolio.objects.all().filter(employeeid=employee)
	professionalskill = EmployeeProfessionalSkill.objects.all().filter(employeeid=employee)
	languageskill = EmployeeLanguageSkill.objects.all().filter(employeeid=employee)
	awards = EmployeeAwards.objects.all().filter(employeeid=employee)
	context = {'employee_reg':current_employee,'education':education,'workexperience':workexperience,'portflio':portflio,'professionalskill':professionalskill,'languageskill':languageskill,'awards':awards,}
	return render(request,'employee/resume.html',context)
