from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('predict',views.predict,name='predict'),
    path('register/',views.register,name='register'),
    path('login/',views.login1,name='login'),
    path('logout/',views.logout1,name='logout'),
    path('check_otp',views.check_otp,name='check_otp'),
]