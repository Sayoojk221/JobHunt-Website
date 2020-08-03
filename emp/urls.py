from django.urls import path
from emp import views

urlpatterns=[
path('',views.home),
path('register/',views.register_both),
path('login/',views.login_both),
path('employerhome/',views.employer_home),
path('employerlogout/',views.employer_logout),
path('employerprofile/',views.employer_profile),
path('employercontact/',views.employer_contactdetails),
path('employersocialnetworks/',views.employer_socialnetworksdetails),
path('postnewjob/',views.postnew_job),
path('employeehome/',views.employee_home),
path('employeeprofile/',views.employee_profile),
path('employeesocialnetworks/',views.employeesocial_networks),
path('employeecontact/',views.employee_contact),
path('employeeresume/',views.employee_resume),
]
