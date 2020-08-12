from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
from jobportal import settings
from emp.models import *
from django.core.mail import send_mail
from emp.decorators import *
from django.core.paginator import Paginator
from emp.utils import render_to_pdf
from django.http import JsonResponse
import datetime
# Create your views here.

def home(request):
	alljobs = EmployerNewJobPost.objects.all().filter(status='active')
	totalcount = EmployerNewJobPost.objects.all().filter(status='active').count()
	todaycount = EmployerNewJobPost.objects.all().filter(createddate__gt=datetime.date.today()).count()
	context = {'totalcount':totalcount,'todaycount':todaycount,'jobs':alljobs}
	return render(request,'home/home.html',context)

@unauthenticated
def register_both(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['pass']
		phone = request.POST['phone']
		usertype = request.POST['usertype']
		employer_existcheck = EmployerRegister.objects.all().filter(companyemail=email).count()
		employee_existcheck = EmployeeRegister.objects.all().filter(email=email).count()
		if usertype == 'Employer' and employer_existcheck == 0:
			employer_details = EmployerRegister(logo='employerlogo/default.jpg',companyname=name,companyemail=email,password=password,phoneno=phone,authentication='pending')
			employer_details.save()
			details = EmployerRegister.objects.filter(companyemail=email)
			for item in details:
				employerid = item.id
			url = f'http://localhost:8000/accountactivation/?id1={employerid}'
			subject = 'welcome to Job Hunt IT Solution'
			message = f'Hi {name}, thank you for registering in Job Hunt IT Solution. Activate Your account click this link {url}'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email ]
			send_mail( subject, message, email_from, recipient_list,fail_silently=False)

			employer_existcheck = 0
			return render(request,'login&register/login.html',{'success':"Successfully registered"})
		elif usertype == 'Candidate' and employee_existcheck == 0:
			employee_details = EmployeeRegister(profileimage='employeeimage/default.jpg',username=name,password=password,email=email,phoneno=phone,authentication='pending')
			employee_details.save()
			details = EmployeeRegister.objects.filter(email=email)
			for item in details:
				employeeid = item.id

			url = f'http://localhost:8000/accountactivation/?id2={employeeid}'
			subject = 'welcome to Job Hunt IT Solution'
			message = f'Hi {name}, thank you for registering in Job Hunt IT Solution. Activate Your account Click this link {url}'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email ]
			send_mail(subject, message, email_from, recipient_list,fail_silently=False)
			employee_existcheck = 0
			return render(request,'login&register/login.html',{'success':"Successfully registered"})
		else:
			if employer_existcheck > 0:
				return render(request,'login&register/register.html',{'error':name+"  already registered "})
			elif employee_existcheck > 0:
				return render(request,'login&register/register.html',{'error':name+"  already registered "})
	else:
	 	return render(request,'login&register/register.html')

@unauthenticated
def account_activation(request):
	employerid = request.GET.get('id1')
	employeeid = request.GET.get('id2')
	if employeeid:
		EmployeeRegister.objects.all().filter(id=employeeid).update(authentication='success')
		return render(request,'login&register/login.html')
	elif employerid:
		EmployerRegister.objects.all().filter(id=employerid).update(authentication='success')
		return render(request,'login&register/login.html')

@unauthenticated
def login_both(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['pass']
		usertype = request.POST.get('usertype')
		employer_existcheck = EmployerRegister.objects.all().filter(companyemail=email,password=password).count()
		employee_existcheck = EmployeeRegister.objects.all().filter(email=email,password=password).count()
		print(usertype)
		if usertype == 'Employer' and employer_existcheck == 1:
			employer_existcheck = 0
			employer_details = EmployerRegister.objects.all().filter(companyemail=email,authentication='success')
			for item in employer_details:
				request.session['employer-id']=item.id
			if employer_details:
				return redirect('/employerprofile/')
			else:
				return render(request,'login&register/login.html',{'error':'Please check '+email+' for activate account'})
		elif usertype == 'Candidate' and employee_existcheck == 1:
			employee_existcheck = 0
			employee_details = EmployeeRegister.objects.all().filter(email=email,authentication='success')
			for item in employee_details:
				request.session['employee-id']=item.id
				employeeid = item.id
			if employee_details:
				employeeid_exist = EmployeePersonalDetails.objects.all().filter(employeeid=employeeid).values_list('employeeid')
				exist_value = 0
				for item in employeeid_exist:
					exist_value = item
				if exist_value == 0:
					employee_foriegn_data = EmployeeRegister.objects.get(id=employeeid)
					personaldetails = EmployeePersonalDetails(employeeid=employee_foriegn_data)  #creating the database for storing
					jobdetails = EmployeeJobDetails(employeeid=employee_foriegn_data)			 #employee personal,job,social details
					socialdetails = EmployeeSocialDetails(employeeid=employee_foriegn_data)
					personaldetails.save()
					jobdetails.save()
					socialdetails.save()
					return redirect('/employeeprofile/')
				else:
					return redirect('/employeeprofile/')
			else:
				return render(request,'login&register/login.html',{'error':'Please check '+email+' for activate account'})
		else:
			return render(request,'login&register/login.html',{'error':email+' not registered '})


	else:
		return render(request,'login&register/login.html')



def password_change(request):
	employerid = request.GET.get('id')
	employeeid = request.GET.get('id2')
	print(employeeid)
	print(employerid)
	if employerid:
		if request.method == 'POST':
			print('post1')
			newpassword = request.POST['new']
			detail = EmployerRegister.objects.all().filter(id=employerid).update(password=newpassword)
			print(post1)
			return render(request,'login&register/login.html')
		else:
			print('else1')
			return render(request,'login&register/changepassword.html')
	elif employeeid:
		if request.method == 'POST':
			print('post2')
			newpassword = request.POST['new']
			print(newpassword)
			EmployeeRegister.objects.all().filter(id=employeeid).update(password=newpassword)
			return render(request,'login&register/login.html')
		else:
			print('else2')
			return render(request,'login&register/changepassword.html')


@unauthenticated
def forgot_password(request):
	if request.method == 'POST':
		email = request.POST['email']
		usertype = request.POST['usertype']
		employee_check = EmployeeRegister.objects.all().filter(email=email)
		employer_check = EmployerRegister.objects.all().filter(companyemail=email)
		if usertype == 'Employer' and employer_check:
			details = EmployerRegister.objects.all().filter(companyemail=email).values_list('id')
			employerid = [i for j in details for i in j]
			url = f'http://localhost:8000/passwordchange/?id={employerid[0]}'
			subject = 'welcome to Job Hunt IT Solution'
			message = f' please change your password Click this link {url}'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email ]
			send_mail(subject, message, email_from, recipient_list,fail_silently=False)
			return render(request,'login&register/login.html',{'success':'Please check your email..'})
		elif usertype == 'Candidate' and employee_check:
			details = EmployeeRegister.objects.all().filter(email=email).values_list('id')
			employeeid = [i for j in details for i in j]
			url = f'http://localhost:8000/passwordchange/?id2={employeeid[0]}'
			subject = 'welcome to Job Hunt IT Solution'
			message = f' please change your password Click this link {url}'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email ]
			send_mail(subject, message, email_from, recipient_list,fail_silently=False)
			return render(request,'login&register/login.html',{'success':'Please check your email..'})
		else:
			if usertype == 'Employer':
				return render(request,'login&register/forgotpassword.html',{'error':email+' not registed'})
			elif usertype == 'Candidate':
				return render(request,'login&register/forgotpassword.html',{'error':email+' not registed'})
	else:

		return render(request,'login&register/forgotpassword.html')

@unauthenticated_employer
def employer_logout(request):
		del request.session['employer-id']
		return redirect('/')

@unauthenticated_employer
def employer_home(request):
	employerid = request.session['employer-id']
	employer_details = EmployerRegister.objects.all().filter(id=employerid)
	context = {'employer_reg':employer_details}
	return render(request,'employer/employerhome.html',context)

@unauthenticated_employer
def employer_profile_edit(request):
	employer = request.session['employer-id']
	jobs = EmployerNewJobPost.objects.all().filter(employerid=employer).values_list('id')
	jobsid = [i for j in jobs for i in j ]
	for item in jobsid:
		expire = EmployerNewJobPost.objects.all().filter(id=item,deadline=datetime.date.today())
		position = EmployerNewJobPost.objects.all().filter(id=item,positionnumber=0)
		if expire:
			EmployerNewJobPost.objects.all().filter(id=item).update(status='inactive')
			expire = False

		if position:
			EmployerNewJobPost.objects.all().filter(id=item).update(status='inactive')
			position = False

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


@unauthenticated_employer
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

@unauthenticated_employer
def employer_socialnetworksdetails(request):
	employer = request.session['employer-id']
	employerid = EmployerRegister.objects.get(id=employer)
	employer_exist = EmployerSocialDetails.objects.all().filter(employerid=employer).values_list('employerid')
	empid = 0
	for item in employer_exist:
			empid = item
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


@unauthenticated_employer_postjob
def postnew_job(request):
	employer = request.session['employer-id']
	if request.method == 'POST':
		employerid = EmployerRegister.objects.get(id=employer)
		jobtitle = request.POST['title']
		description = request.POST['descr']
		email = request.POST['email']
		linkedin = request.POST['linkedin']
		jobtype = request.POST['jobtype']
		salary = request.POST['salary']
		positionno = request.POST['position']
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
		job_detais = EmployerNewJobPost(employerid=employerid,linkedinurl=linkedin,positionnumber=positionno,jobtitle=jobtitle,description=description,email=email,jobtype=jobtype,offerdsalary=salary,careerlevel=level,experience=experience,gender=gender,industry=industry,country=country,city=city,deadline=deadline,requiredknowledge=knowledge,educationandexperience=educationandexperience,status='active')
		job_detais.save()
		return redirect('/postnewjob/')
	else:
		current_employer =EmployerRegister.objects.all().filter(id=employer)
		context = {'employer_reg':current_employer}
		return render(request,'employer/postnewjob.html',context)


@unauthenticated_employee
def employee_home(request):
	employee = request.session['employee-id']
	candidatelist = CandidatesList.objects.all().filter(employeeid=employee).values_list('employeeid')
	value = [j for i in candidatelist for j in i]
	if employee not in value:
		personal_data = EmployeePersonalDetails.objects.all().filter(employeeid=employee).values_list('fullname','country','city')
		job_data = EmployeeJobDetails.objects.all().filter(employeeid=employee).values_list('jobtitle','company')
		v1 = [i for j in personal_data for i in j]
		v2 = [k for i in job_data for k in i]
		if not None in v1 and not 'Nil' in v2:
			job = EmployeeJobDetails.objects.all().filter(employeeid=employee).values_list('id')
			personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee).values_list('id')
			job_id = [j for i in job for j in i]
			personal_id = [j for i in personal for j in i]

			id1 = EmployeeRegister.objects.get(id=employee)
			id2 = EmployeeJobDetails.objects.get(id=job_id[0])
			id3 = EmployeePersonalDetails.objects.get(id=personal_id[0])
			candidate_details = CandidatesList(employeeid=id1,employeepersonalid=id3,employeejobdetailsid=id2,status='failed')
			candidate_details.save()

	alljobs = EmployerNewJobPost.objects.all().filter(status='active')
	count = EmployerNewJobPost.objects.all().filter(status='active').count()
	todaycount = EmployerNewJobPost.objects.all().filter(createddate__gt=datetime.date.today()).count()

	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	context = {'todaycount':todaycount,'jobcount':count,'jobs':alljobs,'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee,'employee_per':personal,'employee_job':job}
	return render(request,'employee/employeehome.html',context)

@unauthenticated_employee
def category_search(request):
	employee = request.session['employee-id']
	key = request.GET.get('key')
	query =  EmployerNewJobPost.objects.all().filter(industry__icontains=key,status='active')
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	context = {'alljobs':query,'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee,'employee_per':personal,'employee_job':job}
	return render(request,'employee/alljobs.html',context)

@unauthenticated_employee
def employee_search(request):
	employee = request.session['employee-id']
	if request.method == 'POST':
		key = request.POST['key']
		location = request.POST['location']
		query =  EmployerNewJobPost.objects.all().filter(jobtitle__icontains=key,country__icontains=location,status='active')
		jobcount = EmployerNewJobPost.objects.all().filter(jobtitle__icontains=key,status='active').count()
		shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
		shortlist = JobShortlists.objects.all().filter(employeeid=employee)
		current_employee = EmployeeRegister.objects.all().filter(id=employee)
		job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
		personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
		context = {'alljobs':query,'count':jobcount,'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee,'employee_per':personal,'employee_job':job}
		return render(request,'employee/alljobs.html',context)

@unauthenticated_employee
def employee_logout(request):
	del request.session['employee-id']
	return redirect('/')

@unauthenticated_employee
def employee_profile(request):
	employee = request.session['employee-id']
	details_check = EmployeePersonalDetails.objects.all().filter(employeeid=employee).values_list('fullname','age','education','city','country','gender')
	education_detail = EmployeeEducation.objects.all().filter(employeeid=employee)
	value = [i for j in details_check for i in j ]
	if not None in value and education_detail:
		shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
		shortlist = JobShortlists.objects.all().filter(employeeid=employee)
		current_employee = EmployeeRegister.objects.all().filter(id=employee)
		job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
		social = EmployeeSocialDetails.objects.all().filter(employeeid=employee)
		personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
		education = EmployeeEducation.objects.all().filter(employeeid=employee)
		workexperience = EmployeeWorkExperience.objects.all().filter(employeeid=employee)
		portflio = EmployeePortfolio.objects.all().filter(employeeid=employee)
		professionalskill = EmployeeProfessionalSkill.objects.all().filter(employeeid=employee)
		languageskill = EmployeeLanguageSkill.objects.all().filter(employeeid=employee)
		awards = EmployeeAwards.objects.all().filter(employeeid=employee)
		context = {'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee,'employee_per':personal,'education':education,'workexperience':workexperience,'portflio':portflio,'professionalskill':professionalskill,'languageskill':languageskill,'awards':awards,'employee_job':job,'employee_social':social}
		return render(request,'employee/singleprofile.html',context)
	else:
		return redirect('/employeeprofile/')

@unauthenticated_employee
def employee_profile_edit(request):
	employee = request.session['employee-id']
	if request.method == 'POST':
		profilepic = request.FILES.get('image')
		fullname = request.POST['fullname']
		company = request.POST['company']
		jobtitle = request.POST['jobtitle']
		salary = request.POST['salary']
		experience = request.POST['exp']
		education = request.POST['edu']
		age = request.POST['age']
		gender = request.POST['gender']
		description = request.POST['desc']

		if profilepic:
			employee_details = EmployeeRegister.objects.get(id=employee)
			employee_details.profileimage = profilepic
			employee_details.save()

		EmployeePersonalDetails.objects.all().filter(employeeid=employee).update(fullname=fullname,age=age,education=education,gender=gender)
		EmployeeJobDetails.objects.all().filter(employeeid=employee).update(company=company,jobtitle=jobtitle,experience=experience,currentsalary=salary,jobdescription=description)
		return redirect('/employeeprofile/')

	else:
		shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
		shortlist = JobShortlists.objects.all().filter(employeeid=employee)
		current_employee = EmployeeRegister.objects.all().filter(id=employee)
		personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
		job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
		social = EmployeeSocialDetails.objects.all().filter(employeeid=employee)
		context = {'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee,'employee_per':personal,'employee_job':job,'employee_social':social}
		return render(request,'employee/profile.html',context)

@unauthenticated_employee
def employeesocial_networks(request):
	employee = request.session['employee-id']
	if request.method == 'POST':
		facebook = request.POST['facebook']
		linkedin = request.POST['linkedin']
		twitter = request.POST['twitter']

		EmployeeSocialDetails.objects.all().filter(employeeid=employee).update(facebook=facebook,linkedin=linkedin,twitter=twitter)
		return redirect('/employeeprofile/')
	else:
		return redirect('/employeeprofile/')

@unauthenticated_employee
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

@unauthenticated_employee
def employee_resume(request):
	employee = request.session['employee-id']
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	education = EmployeeEducation.objects.all().filter(employeeid=employee)
	workexperience = EmployeeWorkExperience.objects.all().filter(employeeid=employee)
	portflio = EmployeePortfolio.objects.all().filter(employeeid=employee)
	professionalskill = EmployeeProfessionalSkill.objects.all().filter(employeeid=employee)
	languageskill = EmployeeLanguageSkill.objects.all().filter(employeeid=employee)
	awards = EmployeeAwards.objects.all().filter(employeeid=employee)
	context = {'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee,'employee_per':personal,'employee_job':job,'education':education,'workexperience':workexperience,'portflio':portflio,'professionalskill':professionalskill,'languageskill':languageskill,'awards':awards,}
	return render(request,'employee/resume.html',context)

@unauthenticated_employee
def employee_education(request):
	employee = request.session['employee-id']
	educationid = request.GET.get('id')
	educationremoveid = request.GET.get('id2')
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	context={'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee}
	if educationid:
		if request.method == 'POST':
			title = request.POST['title']
			course = request.POST['course']
			institute = request.POST['institute']
			startyear = request.POST['startyear']
			endyear = request.POST['endyear']
			description = request.POST['description']
			EmployeeEducation.objects.all().filter(id=educationid).update(title=title,course=course,institute=institute,startyear=startyear,endyear=endyear,description=description)
			return redirect('/employeeresume/')
		else:
			update_details = EmployeeEducation.objects.all().filter(id=educationid)
			return render(request,'employee/addeducation.html',{'employee_reg':current_employee,'update':update_details})

	elif educationremoveid:
		EmployeeEducation.objects.all().filter(id=educationremoveid).delete()
		return redirect('/employeeresume/')

	elif not educationid:
		if request.method == 'POST':
			employee_foriegn_data = EmployeeRegister.objects.get(id=employee)
			title = request.POST['title']
			course = request.POST['course']
			institute = request.POST['institute']
			startyear = request.POST['startyear']
			endyear = request.POST['endyear']
			description = request.POST['description']
			education_details = EmployeeEducation(employeeid=employee_foriegn_data,title=title,course=course,institute=institute,startyear=startyear,endyear=endyear,description=description)
			education_details.save()
			return redirect('/education/')
		else:
			return render(request,'employee/addeducation.html',context)

@unauthenticated_employee
def employee_workexperience(request):
	employee = request.session['employee-id']
	experienceid = request.GET.get('id')
	experienceremoveid = request.GET.get('id2')
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	context={'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee}
	if experienceid:
		if request.method == 'POST':
			job = request.POST['job']
			company = request.POST['company']
			startyear = request.POST['startyear']
			endyear = request.POST['endyear']
			description = request.POST['desc']
			EmployeeWorkExperience.objects.all().filter(id=experienceid).update(job=job,company=company,startyear=startyear,endyear=endyear,jobdescription=description)
			return redirect('/employeeresume/')
		else:
			update_details = EmployeeWorkExperience.objects.all().filter(id=experienceid)
			return render(request,'employee/addexperience.html',{'employee_reg':current_employee,'update':update_details})

	elif experienceremoveid:
		EmployeeWorkExperience.objects.all().filter(id=experienceremoveid).delete()
		return redirect('/employeeresume/')

	elif not experienceid:
		if request.method == 'POST':
			employee_foriegn_data = EmployeeRegister.objects.get(id=employee)
			job = request.POST['job']
			company = request.POST['company']
			startyear = request.POST['startyear']
			endyear = request.POST['endyear']
			description = request.POST['desc']
			experience_details = EmployeeWorkExperience(employeeid=employee_foriegn_data,job=job,company=company,startyear=startyear,endyear=endyear,jobdescription=description)
			experience_details.save()
			return redirect('/workexperience/')
		else:
			return render(request,'employee/addexperience.html',context)

@unauthenticated_employee
def employee_portfolio(request):
	employee = request.session['employee-id']
	portfolioid = request.GET.get('id')
	portfolioremoveid = request.GET.get('id2')
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	context={'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee}

	if portfolioid:
		if request.method == 'POST':
			exist_portfolio_details = EmployeePortfolio.objects.get(id=portfolioid)
			image = request.FILES.get('portfolio')
			url = request.POST['url']
			if image:
				exist_portfolio_details.image = image
				exist_portfolio_details.save()
			EmployeePortfolio.objects.all().filter(id=portfolioid).update(url=url)
			return redirect('/employeeresume/')
		else:
			update_details = EmployeePortfolio.objects.all().filter(id=portfolioid)
			return render(request,'employee/addportfolio.html',{'employee_reg':current_employee,'update':update_details})

	elif portfolioremoveid:
		EmployeePortfolio.objects.all().filter(id=portfolioremoveid).delete()
		return redirect('/employeeresume/')

	elif not portfolioid:
		if request.method == 'POST':
			employee_foriegn_data = EmployeeRegister.objects.get(id=employee)
			image = request.FILES.get('portfolio')
			url = request.POST['url']
			portfolio_details = EmployeePortfolio(employeeid=employee_foriegn_data,url=url,image=image)
			portfolio_details.save()
			return redirect('/portfolio/')

		else:
			return render(request,'employee/addportfolio.html',context)

@unauthenticated_employee
def employee_professionalskill(request):
	employee = request.session['employee-id']
	professionalid = request.GET.get('id')
	professionalremoveid = request.GET.get('id2')
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	context={'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee}

	if professionalid:
		if request.method == 'POST':
			skill = request.POST['skill']
			percentage = request.POST['percentage']
			EmployeeProfessionalSkill.objects.all().filter(id=professionalid).update(skillname=skill,percentage=percentage)
			return redirect('/employeeresume/')
		else:
			update_details = EmployeeProfessionalSkill.objects.all().filter(id=professionalid)
			return render(request,'employee/addprofessionalskills.html',{"employee_reg":current_employee,'update':update_details})

	elif professionalremoveid:
		EmployeeProfessionalSkill.objects.all().filter(id=professionalremoveid).delete()
		return redirect('/employeeresume/')

	elif not professionalid:
		if request.method == 'POST':
			employee_foriegn_data = EmployeeRegister.objects.get(id=employee)
			skill = request.POST['skill']
			percentage = request.POST['percentage']
			professional_details = EmployeeProfessionalSkill(employeeid=employee_foriegn_data,skillname=skill,percentage=percentage)
			professional_details.save()
			return redirect('/professionalskill/')
		else:
			return render(request,'employee/addprofessionalskills.html',context)

@unauthenticated_employee
def employee_languages(request):
	employee = request.session['employee-id']
	languageid = request.GET.get('id')
	languageremoveid = request.GET.get('id2')
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	context={'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee}

	if languageid:
		if request.method == 'POST':
			language = request.POST['language']
			percentage = request.POST['percentage']
			EmployeeLanguageSkill.objects.all().filter(id=languageid).update(language=language,percentage=percentage)
			return redirect('/employeeresume/')
		else:
			update_details = EmployeeLanguageSkill.objects.all().filter(id=languageid)
			return render(request,'employee/addlanguages.html',{"employee_reg":current_employee,'update':update_details})

	elif languageremoveid:
		EmployeeLanguageSkill.objects.all().filter(id=languageremoveid).delete()
		return redirect('/employeeresume/')

	elif not languageid:
		if request.method == 'POST':
			employee_foriegn_data = EmployeeRegister.objects.get(id=employee)
			language = request.POST['language']
			percentage = request.POST['percentage']
			language_details = EmployeeLanguageSkill(employeeid=employee_foriegn_data,language=language,percentage=percentage)
			language_details.save()
			return redirect('/languages/')
		else:
			return render(request,'employee/addlanguages.html',context)

	return render(request,'employee/addlanguages.html')

@unauthenticated_employee
def employee_awards(request):
	employee = request.session['employee-id']
	awardid = request.GET.get('id')
	awardremoveid = request.GET.get('id2')
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	context={'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee}

	if awardid:
		if  request.method == 'POST':
			awardname = request.POST['name']
			year = request.POST['year']
			description = request.POST['description']
			EmployeeAwards.objects.all().filter(id=awardid).update(awardname=awardname,year=year,description=description)
			return redirect('/employeeresume/')

		else:
			update_details = EmployeeAwards.objects.all().filter(id=awardid)
			return render(request,'employee/addawards.html',{"employee_reg":current_employee,'update':update_details})

	elif awardremoveid:
		EmployeeAwards.objects.all().filter(id=awardremoveid).delete()
		return redirect('/employeeresume/')

	elif not awardid:
		if  request.method == 'POST':
			employee_foriegn_data = EmployeeRegister.objects.get(id=employee)
			awardname = request.POST['name']
			year = request.POST['year']
			description = request.POST['description']
			award_details = EmployeeAwards(employeeid=employee_foriegn_data,awardname=awardname,year=year,description=description)
			award_details.save()
			return redirect('/awards/')
		else:
			return render(request,'employee/addawards.html',context)



@unauthenticated_employer
def candidates_list(request):
	employer = request.session['employer-id']
	details = deletedcandidates.objects.all().filter(employerid=employer).values_list('employeeid')
	deleted_list = [i for j in details for i in j]
	current_employer = EmployerRegister.objects.all().filter(id=employer)
	if request.method == 'POST':
		key = request.POST['key']


		candidate_details = CandidatesList.objects.all().filter(employeejobdetailsid__jobtitle__icontains=key,status='failed')

		context = {'list':deleted_list,'employer_reg':current_employer,'candidate':candidate_details}
		return render(request,'employer/candidates.html',context)
	else:
		candidate_details = CandidatesList.objects.all().filter(status='failed')
		context = {'list':deleted_list,'employer_reg':current_employer,'candidate':candidate_details}
		return render(request,'employer/candidates.html',context)

@unauthenticated_employee
def employee_jobsingle(request):
	employee = request.session['employee-id']
	job_id = request.GET.get('id')

	jobid_exist = JobApplication.objects.all().filter(employeeid=employee,jobid=job_id)
	if jobid_exist:
		exist = True
	else:
		exist = False
	totalapplication = JobApplication.objects.all().filter(jobid=job_id).count()
	alljobs = EmployerNewJobPost.objects.all().filter(status='active').order_by('-id')
	job_details = EmployerNewJobPost.objects.all().filter(id=job_id)
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	employee_job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	context = {'applicationcount':totalapplication,'count':shortlistcount,'shortlist':shortlist,'exist':exist,'alljobs':alljobs,'job':job_details,'employee_reg':current_employee,'employee_per':personal,'employee_job':employee_job}
	return render(request,'employee/job.html',context)

@unauthenticated_employee
def employee_alljobs(request):
	employee = request.session['employee-id']
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	alljobs = EmployerNewJobPost.objects.all().filter(status='active')

	jobcount = EmployerNewJobPost.objects.all().filter(status='active').count()
	employee_job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	context = {'count':shortlistcount,'shortlist':shortlist,'alljobs':alljobs,'count':jobcount,'employee_reg':current_employee,'employee_per':personal,'employee_job':employee_job}
	return render(request,'employee/alljobs.html',context)

@unauthenticated_employee
def employer_singleprofile(request):
	employee = request.session['employee-id']
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	employerid = request.GET.get('id')
	employersocial = EmployerSocialDetails.objects.all().filter(employerid=employerid)
	postedjobcount = EmployerNewJobPost.objects.all().filter(employerid=employerid).count()
	postedjobs = EmployerNewJobPost.objects.all().filter(employerid=employerid)
	employer_details = EmployerRegister.objects.all().filter(id=employerid)
	employee_job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	context = {'count':shortlistcount,'shortlist':shortlist,'employersocial':employersocial,'postedjobs':postedjobs,'count':postedjobcount,'employer':employer_details,'employee_reg':current_employee,'employee_per':personal,'employee_job':employee_job}
	return render(request,'employee/employerdetails.html',context)

@unauthenticated_employee
def total_employers(request):
	employee = request.session['employee-id']
	details = EmployerNewJobPost.objects.all().values_list('employerid')
	total_employer = [i for j in details for i in j]
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	employee_job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	totalemployercount = EmployerRegister.objects.all().count()
	totalemployer_details = EmployerRegister.objects.all()
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	context = {'employerlist':total_employer,'count':shortlistcount,'shortlist':shortlist,'employercount':totalemployercount,'employerdetails':totalemployer_details,'employee_reg':current_employee,'employee_per':personal,'employee_job':employee_job}
	return render(request,'employee/employers.html',context)

@unauthenticated_employee
def job_apply(request):
	employee = request.session['employee-id']
	jobid = request.GET.get('id')
	jobremoveid = request.GET.get('removeid')
	if jobremoveid:
		JobApplication.objects.all().filter(id=jobremoveid,employeeid=employee).delete()
		return redirect('/appliedjobs/')
	employee_details = EmployeeRegister.objects.get(id=employee)
	employee_personal = EmployeePersonalDetails.objects.get(employeeid=employee)
	employee_job = EmployeeJobDetails.objects.get(employeeid=employee)
	job_details = EmployerNewJobPost.objects.get(id=jobid)
	application_details = JobApplication(employeepersonalid=employee_personal,employeejobdetails=employee_job,employeeid=employee_details,jobid=job_details,status='pending')
	application_details.save()
	return redirect('/appliedjobs/')

@unauthenticated_employee
def applied_jobs(request):
	employee = request.session['employee-id']
	appliedjobs = JobApplication.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	context = {'count':shortlistcount,'shortlist':shortlist,'employee_job':job,'employee_reg':current_employee,'employee_per':personal,'applied':appliedjobs}
	return render(request,'employee/appliedjobs.html',context)

@unauthenticated_employee
def jobshortlist_apply(request):
	employee = request.session['employee-id']
	shortlistid = request.GET.get('id2')
	shorlistremoveid = request.GET.get('removeid')

	if shorlistremoveid:
		JobShortlists.objects.all().filter(id=shorlistremoveid,employeeid=employee).delete()
		return redirect('/jobshortlist/')

	shortlist_exist = JobShortlists.objects.all().filter(employeeid=employee,shortlistedjobid=shortlistid)
	if shortlist_exist:
		return redirect('/alljobs/')
	else:
		employee_details = EmployeeRegister.objects.get(id=employee)
		job_details = EmployerNewJobPost.objects.get(id=shortlistid)
		shortlist_details = JobShortlists(employeeid=employee_details,shortlistedjobid=job_details,status='shortlisted')
		shortlist_details.save()
		return redirect('/alljobs/')

@unauthenticated_employee
def shortlisted_jobs(request):
	employee = request.session['employee-id']
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	shortlists = JobShortlists.objects.all().filter(employeeid=employee,status='shortlisted')
	context = {'count':shortlistcount,'shortlist':shortlist,'employee_job':job,'employee_reg':current_employee,'employee_per':personal,'shortlist':shortlists}
	return render(request,'employee/jobshortlists.html',context)


@unauthenticated_employer
def employeeprofile_shortlist(request):
	employer = request.session['employer-id']
	profileshortlistid = request.GET.get('id')
	personaldetails_id = EmployeePersonalDetails.objects.all().filter(employeeid=profileshortlistid).values_list('id')
	jobdetails_id = EmployeeJobDetails.objects.all().filter(employeeid=profileshortlistid).values_list('id')
	id1 = [item for i in personaldetails_id for item in i]
	id2 = [item for j in jobdetails_id for item in j]
	employee_detail = EmployeeRegister.objects.get(id=profileshortlistid)
	employer_detail = EmployerRegister.objects.get(id=employer)
	employee_personal = EmployeePersonalDetails.objects.get(id=id1[0])
	employee_job = EmployeeJobDetails.objects.get(id=id2[0])
	details = EmployeeProfileShortlists.objects.all().filter(employerid=employer,employeeid=profileshortlistid)
	if not details:
		profileshortlist_details = EmployeeProfileShortlists(employeejobid=employee_job,employeepersonalid=employee_personal,employerid=employer_detail,employeeid=employee_detail)
		profileshortlist_details.save()

	return redirect('/candidates/')

@unauthenticated_employer
def resume_lists(request):
	employer = request.session['employer-id']
	removeid = request.GET.get('id')
	if removeid:
		employeeid = EmployeeProfileShortlists.objects.all().filter(id=removeid).values_list('employeeid')
		id1 = [i for j in employeeid for i in j]
		employee_details = EmployeeRegister.objects.get(id=id1[0])
		employer_details = EmployerRegister.objects.get(id=employer)
		save_deletedetails = deletedcandidates(employerid=employer_details,employeeid=employee_details)
		save_deletedetails.save()
		EmployeeProfileShortlists.objects.all().filter(id=removeid).delete()
		return redirect('/resumelists/')
	current_employer = EmployerRegister.objects.all().filter(id=employer)
	resumelists = EmployeeProfileShortlists.objects.all().filter(employerid=employer)
	context = {'employer_reg':current_employer,'resume':resumelists}
	return render(request,'employer/resume.html',context)


@unauthenticated_employer
def interview_message(request):
	if request.method == 'POST':
		incomingrequest = request.POST.get('test')
		companyname = request.POST['company']
		employeeemail = request.POST['email']
		companyemail = request.POST['companyemail']
		contactno = request.POST['phone']
		message1 = request.POST['message']

		subject=f'{companyname} Interview Availability'
		message = message1
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [employeeemail]
		send_mail(subject, message, email_from, recipient_list,fail_silently=False)
		if incomingrequest:
			return redirect('/incomingapplication/')
		else:
			return redirect('/resumelists/')


@unauthenticated_employer
def employeeprofile_view(request):
	employeeid = request.GET.get('id')

	employer = request.session['employer-id']
	current_employer = EmployerRegister.objects.all().filter(id=employer)
	job = EmployeeJobDetails.objects.all().filter(employeeid=employeeid)
	social = EmployeeSocialDetails.objects.all().filter(employeeid=employeeid)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employeeid)
	education = EmployeeEducation.objects.all().filter(employeeid=employeeid)
	workexperience = EmployeeWorkExperience.objects.all().filter(employeeid=employeeid)
	portflio = EmployeePortfolio.objects.all().filter(employeeid=employeeid)
	professionalskill = EmployeeProfessionalSkill.objects.all().filter(employeeid=employeeid)
	languageskill = EmployeeLanguageSkill.objects.all().filter(employeeid=employeeid)
	awards = EmployeeAwards.objects.all().filter(employeeid=employeeid)
	context = {'employer_reg':current_employer,'employee_per':personal,'education':education,'workexperience':workexperience,'portflio':portflio,'professionalskill':professionalskill,'languageskill':languageskill,'awards':awards,'employee_job':job,'employee_social':social}
	return render(request,'employer/employeeprofile.html',context)


@unauthenticated_employee
def employee_cv(request):
	employee = request.session['employee-id']
	shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
	shortlist = JobShortlists.objects.all().filter(employeeid=employee)
	current_employee = EmployeeRegister.objects.all().filter(id=employee)
	employee_job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
	cv_exist = EmployeeCoverLetter.objects.all().filter(employeeid=employee)
	context = {'count':shortlistcount,'shortlist':shortlist,'cv':cv_exist,'employee_reg':current_employee,'employee_per':personal,'employee_job':employee_job}
	if cv_exist:
		if request.method == 'POST':
			description = request.POST['cv']
			EmployeeCoverLetter.objects.all().filter(employeeid=employee).update(description=description)
			return redirect('/employeecv/')
		else:
			return render(request,'employee/employeecv.html',context)
	else:
		if request.method == 'POST':
			employee_details = EmployeeRegister.objects.get(id=employee)
			description = request.POST['cv']
			cv_details = EmployeeCoverLetter(employeeid=employee_details,description=description)
			cv_details.save()
			return redirect('/employeecv/')
		else:
			return render(request,'employee/employeecv.html',context)

@unauthenticated_download
def download_pdf(request):
	employeeid = request.GET.get('id')
	job = EmployeeJobDetails.objects.all().filter(employeeid=employeeid)
	social = EmployeeSocialDetails.objects.all().filter(employeeid=employeeid)
	personal = EmployeePersonalDetails.objects.all().filter(employeeid=employeeid)
	education = EmployeeEducation.objects.all().filter(employeeid=employeeid)
	workexperience = EmployeeWorkExperience.objects.all().filter(employeeid=employeeid)
	professionalskill = EmployeeProfessionalSkill.objects.all().filter(employeeid=employeeid)
	languageskill = EmployeeLanguageSkill.objects.all().filter(employeeid=employeeid)
	awards = EmployeeAwards.objects.all().filter(employeeid=employeeid)
	context = {'employee_per':personal,'education':education,'workexperience':workexperience,'professionalskill':professionalskill,'languageskill':languageskill,'awards':awards,'employee_job':job,'employee_social':social}
	template = loader.get_template('employer/downloadpdf.html')
	html = template.render(context)
	pdf = render_to_pdf('employer/downloadpdf.html', context)
	if pdf:
        	response = HttpResponse(pdf, content_type='application/pdf')
        	filename = "emp.pdf"
        	content = "inline; filename=%s" %(filename)
        	download = request.GET.get("download")
        	if download:
            		content = "attachment; filename='%s'" %(filename)
        	response['Content-Disposition'] = content
        	return response

@unauthenticated_employer
def candidate_search(request):
	value = request.GET.get('value')
	details = CandidatesList.objects.all().filter(employeejobdetailsid__jobtitle__contain=value,status='failed')
	context = {'candidate':details}
	return JsonResponse(context)

@unauthenticated_employer
def search(request):
	employer = request.session['employer-id']
	current_employer = EmployerRegister.objects.all().filter(id=employer)
	details = deletedcandidates.objects.all().filter(employerid=employer).values_list('employeeid')
	deleted_list = [i for j in details for i in j]
	if request.method == 'POST':
		key = request.POST['key']
		location = request.POST['location']
		details = CandidatesList.objects.all().filter(employeejobdetailsid__jobtitle__icontains=key,employeepersonalid__country__icontains=location,status='failed')
		print(details)
		context = {'list':deleted_list,'employer_reg':current_employer,'candidate':details}
		return render(request,'employer/candidates.html',context)

@unauthenticated_employer
def employerjob_manage(request):
	employer = request.session['employer-id']
	current_employer = EmployerRegister.objects.all().filter(id=employer)
	active_jobs = EmployerNewJobPost.objects.all().filter(employerid=employer,status='active').count()
	totaljobs = EmployerNewJobPost.objects.all().filter(employerid=employer).count()
	totalapplications = JobApplication.objects.all().filter(jobid__employerid__id=employer).count()
	job_details = EmployerNewJobPost.objects.all().filter(employerid=employer)
	context = {'active':active_jobs,'details':job_details,'employer_reg':current_employer,'totaljobs':totaljobs,'applications':totalapplications}
	return render(request,'employer/jobmanage.html',context)

@unauthenticated_employer
def employerjobsingle_view(request):
	employer = request.session['employer-id']
	jobid = request.GET.get('id')
	jobremoveid = request.GET.get('id2')
	if jobremoveid:
		EmployerNewJobPost.objects.all().filter(id=jobremoveid).delete()
		return redirect('/employerjobmanage/')
	totalapplication = JobApplication.objects.all().filter(jobid=jobid).count()
	job_details = EmployerNewJobPost.objects.all().filter(id=jobid)
	current_employer = EmployerRegister.objects.all().filter(id=employer)
	context = {'applicationcount':totalapplication,'employer_reg':current_employer,'job':job_details}
	return render(request,'employer/jobsingle.html',context)

@unauthenticated_employer
def job_edit(request):
	employer = request.session['employer-id']
	current_employer = EmployerRegister.objects.all().filter(id=employer)
	jobid = request.GET.get('id')
	if request.method == 'POST':
		job_id = request.POST['job']
		employerid = EmployerRegister.objects.get(id=employer)
		jobtitle = request.POST['title']
		description = request.POST['descr']
		email = request.POST['email']
		linkedin = request.POST['linkedin']
		jobtype = request.POST['jobtype']
		salary = request.POST['salary']
		positionno = request.POST['position']
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
		print(job_id)
		EmployerNewJobPost.objects.all().filter(id=job_id).update(linkedinurl=linkedin,positionnumber=positionno,jobtitle=jobtitle,description=description,email=email,jobtype=jobtype,offerdsalary=salary,careerlevel=level,experience=experience,gender=gender,industry=industry,country=country,city=city,deadline=deadline,requiredknowledge=knowledge,educationandexperience=educationandexperience)
		return redirect('/employerjobmanage/')
	else:
		job_details = EmployerNewJobPost.objects.all().filter(id=jobid)
		context = {'employer_reg':current_employer,'job':job_details}
		return render(request,'employer/jobedit.html',context)

@unauthenticated_employer
def incoming_application(request):
	employer = request.session['employer-id']
	removeid = request.GET.get('id')
	if removeid:
		JobApplication.objects.all().filter(id=removeid).delete()
		return redirect('/incomingapplication/')
	current_employer = EmployerRegister.objects.all().filter(id=employer)
	jobapplication = JobApplication.objects.all().filter(jobid__employerid=employer,status='pending')
	context = {'employer_reg':current_employer,'job':jobapplication}

	return render(request,'employer/incomingapplication.html',context)

@unauthenticated_employer
def employerchange_password(request):
	employer = request.session['employer-id']
	if request.method == 'POST':
		old= request.POST['old']
		oldpassword  = EmployerRegister.objects.all().filter(id=employer,password=old)
		if oldpassword:
			new = request.POST['password']
			EmployerRegister.objects.all().filter(id=employer).update(password=new)
			return redirect('/employerchangepassword//')
		else:
			current_employer = EmployerRegister.objects.all().filter(id=employer)
			return render(request,'employer/changepassword.html',{'employer_reg':current_employer,'error':'old password mismatch'})
	else:
		current_employer = EmployerRegister.objects.all().filter(id=employer)
		context = {'employer_reg':current_employer}
		return render(request,'employer/changepassword.html',context)

@unauthenticated_employee
def employeechange_password(request):
	employee = request.session['employee-id']
	if request.method == 'POST':
		old= request.POST['old']
		oldpassword  = EmployeeRegister.objects.all().filter(id=employee,password=old)
		if oldpassword:
			new = request.POST['newpass']
			EmployeeRegister.objects.all().filter(id=employee).update(password=new)
			return redirect('/employeechangepassword/')
		else:
			current_employee = EmployeeRegister.objects.all().filter(id=employee)
			return render(request,'employee/changepassword.html',{'employee_reg':current_employee,'error':'old password mismatch'})
	else:
		shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
		shortlist = JobShortlists.objects.all().filter(employeeid=employee)
		current_employee = EmployeeRegister.objects.all().filter(id=employee)
		context = {'count':shortlistcount,'shortlist':shortlist,'employee_reg':current_employee}
		return render(request,'employee/changepassword.html',context)

@unauthenticated_employee
def messageto_employer(request):
	employee = request.session['employee-id']
	if request.method == 'POST':
		job_id = request.POST['jobid']
		companymail = request.POST['companymail']
		name = request.POST['name']
		email = request.POST['email']
		phonenumber = request.POST['phone']
		message1 = request.POST['message']

		subject=f'Job Detials Enquiry'
		message = message1
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [companymail]
		send_mail(subject, message, email_from, recipient_list,fail_silently=False)

		jobid_exist = JobApplication.objects.all().filter(employeeid=employee,jobid=job_id)
		if jobid_exist:
			exist = True
		else:
			exist = False
		alljobs = EmployerNewJobPost.objects.all().filter(status='active').order_by('-id')
		job_details = EmployerNewJobPost.objects.all().filter(id=job_id)
		shortlistcount = JobShortlists.objects.all().filter(employeeid=employee).count()
		shortlist = JobShortlists.objects.all().filter(employeeid=employee)
		current_employee = EmployeeRegister.objects.all().filter(id=employee)
		employee_job = EmployeeJobDetails.objects.all().filter(employeeid=employee)
		personal = EmployeePersonalDetails.objects.all().filter(employeeid=employee)
		context = {'alljobs':alljobs,'count':shortlistcount,'shortlist':shortlist,'exist':exist,'job':job_details,'employee_reg':current_employee,'employee_per':personal,'employee_job':employee_job}
		return render(request,'employee/job.html',context)


@unauthenticated_employer
def interview_selection(request):
	employer = request.session['employer-id']
	passedid = request.GET.get('id')
	rejectid = request.GET.get('id1')
	if passedid:
		value = JobApplication.objects.all().filter(id=passedid).values_list('employeeid','jobid','employeepersonalid__fullname','jobid__jobtitle','jobid__employerid__companyname','employeeid__email')
		allid = [i for j in value for i in j]

		subject = f'Job offer from {allid[4]}'
		message = f'Dear {allid[2]}, {allid[4]} is pleased to offer you the position of {allid[3]}, Your skill will be an ideal fit for our company requirement. As we discussed , your starting date will be june 1, 2020 . you will present on that date, Thank you '

		email_from = settings.EMAIL_HOST_USER

		recipient_list = [allid[5],]
		send_mail(subject, message, email_from, recipient_list,fail_silently=False)


		JobApplication.objects.all().filter(employeeid__id=allid[0],jobid__id=allid[1]).update(status='Passed')
		value1 = EmployerNewJobPost.objects.all().filter(id=allid[1]).values_list('positionnumber')
		totalposition = [i for j in value1 for i in j]
		lastnumber = int(totalposition[0]) - 1
		EmployerNewJobPost.objects.all().filter(id=allid[1]).update(positionnumber=lastnumber)



		return redirect('/incomingapplication/')
	elif rejectid:
		value = JobApplication.objects.all().filter(id=rejectid).values_list('employeeid','jobid')
		allid = [i for j in value for i in j]
		JobApplication.objects.all().filter(employeeid=allid[0],jobid=allid[1]).update(status='Rejected')
		return redirect('/incomingapplication/')

@unauthenticated_employer
def employer_dashboard(request):
	employer = request.session['employer-id']
	details = EmployerRegister.objects.all().filter(id=employer).values_list('country','state','since','teamsize','category','website','description')
	value = [i for j in details for i in j]
	if not None in value:
		current_employer = EmployerRegister.objects.all().filter(id=employer)
		employersocial = EmployerSocialDetails.objects.all().filter(employerid=employer)
		postedjobcount = EmployerNewJobPost.objects.all().filter(employerid=employer).count()
		postedjobs = EmployerNewJobPost.objects.all().filter(employerid=employer)
		employer_details = EmployerRegister.objects.all().filter(id=employer)
		context = {'employersocial':employersocial,'postedjobs':postedjobs,'count':postedjobcount,'employer':employer_details,'employer_reg':current_employer}
		return render(request,'employer/dashboard.html',context)
	else:
		return redirect('/employerprofile/')

