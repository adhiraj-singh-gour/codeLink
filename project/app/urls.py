from django.urls import path,include
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('courses/',courses,name='courses'),
    path('login/',login,name='loginpage'),
    path('playlist/',playlist,name='playlist'),
    path('profile/',profile,name='profile'),
    path('register/',register,name='registerpage'),
    path('teacher_profile/',teacher_profile,name='teacher_profile'),
    path('teachers/',teachers,name='teachers'),
    path('update/',update,name='update'),
    path('watch_video/',watch_video,name='watch-video'),

    # User Registration
    path('user_register/',user_register,name='user_register'),
    path('userLogin',userLogin,name='userLogin'),
    path('verify_user',verify_user,name='verify_user'),
    path('contact/', contact, name='contact'),
    path('teacher_register/',teacher_register,name='teacher_register'),
    path('teacher_register_form/',teacher_register_form,name='teacher_register_form'),
    path('success/',success,name='success'),
    path('forget_pass/',forget_pass,name='forget_pass'),
    path('forget_pass_otp/',forget_pass_otp,name='forget_pass_otp'),
    path('verify_reset_otp/',verify_reset_otp,name='verify_reset_otp'),
    path('verify_new_pass/',verify_new_pass,name='verify_new_pass'),
    path('new_password/',new_password,name='new_password'),


    # path("checkout/",checkout,name='checkout'),
   
]
