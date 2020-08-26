from django.urls import path
from . import views

urlpatterns=[
path('',views.authencation),
path('login/',views.loginadmin),
path('home/',views.home),
path('logout/',views.logout),
path('totalemployee/',views.employees),
path('totalemployer/',views.employers),
path('activelog/',views.active_log),
path('singleemployee/',views.single_employee),
path('singleemployer/',views.single_employer),
]
