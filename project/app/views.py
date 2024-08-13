from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
import random


# Create your views here.
def home(request):
    return render(request, "home1.html")

def home1(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def courses(request):
    return render(request, "courses.html")


def login(request):
    return render(request, "login.html")


def playlist(request):
    course = Course.objects.all()
    video_list = Video.objects.all()
    paginator = Paginator(video_list, 5)
    page_number = request.GET.get('page')
    videos = paginator.get_page(page_number)
    context = {
        "course": course,
        "videos": videos,  
    }
    return render(request, "playlist.html", context)


def profile(request):
    return render(request, "profile.html")


def register(request):
    return render(request, "register.html")


def teacher_profile(request):
    return render(request, "teacher_profile.html")


def teachers(request):
    return render(request, "teachers.html")


def update(request):
    return render(request, "update.html")


def watch_video(request):
    return render(request, "watch-video.html")

def success(request):
    return render(request, "success.html")


# User Registration
def user_register(request):
    if request.method == "POST":
        Name = request.POST.get("name")
        Email = request.POST.get("email")
        Password = request.POST.get("pass")
        Cpassword = request.POST.get("c_pass")
        Profile = request.FILES.get("profile")
        user = Userregister.objects.filter(Email=Email)

        if user:
            message = "User already exist"
            return render(request, "register.html", {"msg": message})
        else:
            if Password == Cpassword:
                user = Userregister.objects.create(
                    Name=Name,
                    Email=Email,
                    Password=Password,
                    Cpassword=Cpassword,
                    Profile=Profile,
                )
                # user.save()
                message = "User register Successfully"
                return render(request, "login.html", {"msg": message})
            else:
                message = "Password not match"
                return render(request, "register.html", {"msg": message})


# User Login
def userLogin(request):
    if request.method == "POST":
        Email = request.POST.get("email")
        Password = request.POST.get("pass")
        user = Userregister.objects.filter(Email=Email)
        
        if user:
            data = Userregister.objects.get(Email=Email)
            if data.Password == Password:
                # Generate OTP
                otp = random.randint(100000, 999999)
                
                # Save OTP to the session
                request.session['otp'] = otp
                request.session['email'] = Email
                
                # Send OTP to the user's email
                send_mail(
                    'Your OTP for Login',
                    f'Your OTP is {otp}',
                    'adhirajsingh31032003@gmail.com',  # replace with your email
                    [Email],
                    fail_silently=False,
                )
                
                # Redirect to OTP verification page
                return render(request, "otp-verification.html", {"email": Email})
            else:
                message = "Password not match"
                return render(request, "login.html", {"msg": message})
        else:
            message = "User not exist"
            return render(request, "register.html", {"msg": message})

    return render(request, "login.html")
        

def verify_user(request):
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        otp_saved = request.session.get('otp')
        Email = request.session.get('email')
        
        if otp_input and otp_saved and str(otp_input) == str(otp_saved):
            data = Userregister.objects.get(Email=Email)
            user = {
                'Name': data.Name,
                'Email': data.Email,
                'Profile': data.Profile
            }
            
            # Clear OTP from session
            del request.session['otp']
            
            return render(request, "home.html", user)
        else:
            message = "Invalid OTP. Please try again."
            return render(request, "otp-verification.html", {"msg": message, "email": Email})
    
    return render(request, "otp-verification.html")    
# =================================================================================================
# =================================================================================================



                # This is Forget password and Email Verification Section
# ==================================================================================================
# ==================================================================================================
OTP = None
RESET_EMAIL = None

def forget_pass(request):
    return render(request, "forgetpass.html")

def new_password(request):
    return render(request, "newpassword.html")

def forget_pass_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = Userregister.objects.filter(Email=email).first()

        if user:
            OTP = random.randint(100000, 999999)  # Generate OTP
            request.session['OTP'] = OTP
            request.session['RESET_EMAIL'] = email

            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP is {OTP}',
                'adhirajsingh31032003@gmail.com',  # Replace with your sender email
                [email],
                fail_silently=False,
            )
            return render(request, 'forgetpass-otp.html')
        else:
            messages.error(request, "Email does not exist")
            return redirect('forget_pass')

    return render(request, 'forget_pass.html')


def verify_reset_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('OTP')

        if stored_otp and entered_otp == str(stored_otp):
            return render(request, 'newpassword.html')
        else:
            messages.error(request, "OTP does not match")
            return redirect('forget_pass_otp')

    return redirect('forget_pass_otp')


def verify_new_pass(request):
    if request.method == "POST":
        entered_new_pass = request.POST.get('newpass')
        entered_c_new_pass = request.POST.get('c-newpass')
        email = request.session.get('RESET_EMAIL')

        if entered_new_pass == entered_c_new_pass:
            user = Userregister.objects.filter(Q(Email__iexact=email)).first()

            if user:
                user.Password = entered_new_pass
                user.Cpassword = entered_c_new_pass
                user.save()
                messages.success(request, "Password updated successfully")
                return render(request,'login.html')
            else:
                messages.error(request, "User does not exist")
                return redirect('new_password')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('new_password')

    return redirect('new_password')

#===================================================================================================
#===================================================================================================  
                     # End Forget Password And Email Verification  Section



                            # This is Contact Information Section
# ===================================================================================================
# ===================================================================================================
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        message = request.POST.get('msg')
        contact_submission = Contact(
            name=name,
            email=email,
            number=number,
            message=message
        )
        contact_submission.save()
        subject = 'New Contact Form Submission'
        message_body = f'Name: {name}\nEmail: {email}\nNumber: {number}\nMessage: {message}'
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message_body, email, recipient_list, fail_silently=False)
    return render(request, 'contact.html')

# ====================================================================================================
# ====================================================================================================
                         # End Contact Information Section




                         # This is the teacher Registration Section
# ===================================================================================================
# ===================================================================================================
def teacher_register_form(request):
    return render(request,'teacher_registration.html')

def teacher_register(request):
    if request.method=="POST":
        name= request.POST.get('name')
        email= request.POST.get('email')
        interested_profile= request.POST.get('profile')
        years_of_experience= request.POST.get('experience')
        previous_institute= request.POST.get('institute')
        current_ctc= request.POST.get('ctc')
        expected_ctc= request.POST.get('e_ctc')
        resume= request.FILES.get('resume')
        user = TeacherRegisterForm.objects.filter(email=email)
        if user:
            message="Teacher already exist"
            return render(request, "teacher_registration.html", {"msg": message})
        else:
            teacher_registration=TeacherRegisterForm(
                name=name,
                email=email,
                interested_profile=interested_profile,
                years_of_experience=years_of_experience,
                previous_institute=previous_institute,
                expected_ctc=expected_ctc,
                current_ctc=current_ctc,
                resume= resume
                )
            teacher_registration.save()
            if email:
                send_mail(
                    'Thank you for applying!',
                    'Thank you for applying to our service. We will get back to you shortly.',
                    'adhirajsingh31032003@gmail.com',  # From email
                    [email],  # To email
                    fail_silently=False,
                )
            return render(request,'success.html')  
            # return HttpResponse('success') 
    return render(request,'teacher_registration.html')  
# ===================================================================================================
# ===================================================================================================  