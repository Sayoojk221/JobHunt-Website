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
path('employersocialnetworks/',views.employer_socialnetworksdetails)
]
