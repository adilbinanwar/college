from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login
from .models import Course, Student, Teacher
from django.contrib.auth.decorators import login_required
import os

# Create your views here.
def home(request):
    return render(request, 'home.html')

def loginpage(request):
    return render(request, 'loginpage.html')

# def loginfun(request):
#     if request.method=='POST':
#         username=request.POST['usname']
#         password=request.POST['passd']
#         user=auth.authenticate(username=username,password=password)
#         if user is not None:
#             if user.is_staff:
#                 login(request,user)
#                 return redirect('adminpage')
#             else:
#                 login(request,user)
#                 auth.login(request,user)
#                 return redirect('userpage')
#         else:
#             messages.info(request,'Invalid Username or Password')
#             return redirect('home')
#     return render(request,'home.html')

def loginfun(request):
    if request.method == 'POST':
        username = request.POST['usname']
        password = request.POST['passd']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_authenticated:  # Check if the user is authenticated
                if user.is_staff:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    messages.info(request, f'Login Successfull')
                    return redirect('adminpage')
                else:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    messages.info(request, f'Login Successfull')
                    return redirect('userpage')  # Redirect to techhome after login
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('loginpage')
    return render(request, 'loginpage.html')

def logoutfun(request):
    auth.logout(request)
    return render(request, 'home.html')


@login_required(login_url='home')
def adminpage(request):
    return render(request, 'adminpage.html')

def regcourse(request):
    if request.method=='POST':
        crsname=request.POST['Course']
        fees=request.POST['Fees']
        crs=Course(coursename=crsname, fees=fees)
        messages.info(request,'Course Added Successfully')
        crs.save()
    return redirect('adminpage')

def stdreg(request):
    crs=Course.objects.all()
    return render(request, 'stdreg.html', {'cou':crs})

def addstd(request):
    if request.method=='POST':
        stdname=request.POST['Stdname']
        age=request.POST['Age']
        address=request.POST['Address']
        doj=request.POST['Doj']
        crs=request.POST['course']
        c=Course.objects.get(id=crs)
        std=Student(studentname=stdname, address=address, age=age, joiningdate=doj, course=c)
        messages.info(request,'Student Added Successfully')
        std.save()
    return redirect('show')

def show(request):
    std = Student.objects.all()
    return render(request, 'show.html', {'std':std})

def showcou(request):
    cou = Course.objects.all()
    return render(request, 'showcou.html', {'c':cou})

def showtchr(request):
    tchr = Teacher.objects.all()
    return render(request, 'showtchr.html', {'c':tchr})

def editstd(request,s):
    st=Student.objects.get(id=s)
    c=Course.objects.all()
    return render(request, 'editstd.html', {'std':st, 'cou':c})

def edit(request,s):
    if request.method == 'POST':
        std=Student.objects.get(id=s)
        std.studentname=request.POST['Stdname']
        std.age=request.POST['Age']
        std.address=request.POST['Address']
        std.joiningdate=request.POST['Doj']
        crs=request.POST['course']
        c=Course.objects.get(id=crs)
        std.course=c
        messages.info(request,'Student Updated Successfully')
        std.save()
    return redirect('show')

def editcou(request,c):
    co=Course.objects.get(id=c)
    return render(request, 'editcou.html', {'cou':co})

def couedit(request,c):
    if request.method == 'POST':
        cou=Course.objects.get(id=c)
        cou.coursename=request.POST['Course']
        cou.fees=request.POST['Fees']
        messages.info(request,'Course Updated Successfully')
        cou.save()
    return redirect('showcou')

def delete(request,s):
    std=Student.objects.get(id=s)
    messages.info(request,'Student Deleted Successfully')
    std.delete()
    return redirect('show')

def deletecou(request,c):
    cou=Course.objects.get(id=c)
    messages.info(request,'Course Deleted Successfully')
    cou.delete()
    return redirect('showcou')

def deletetchr(request,t):
    tchr=Teacher.objects.get(id=t)
    z=tchr.user_id
    u=User.objects.get(id=z)
    os.remove(tchr.image.path)
    messages.info(request,'Teacher Deleted Successfully')
    tchr.delete()
    u.delete()
    return redirect('showtchr')

def signuppage(request):
    crs=Course.objects.all()
    return render(request, 'signuppage.html', {'cou':crs})

def createtchr(request):
    if request.method=='POST': 
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        user_name=request.POST['uname']
        password=request.POST['pass']
        cpassword=request.POST['cpass']
        email=request.POST['mail']
        age=request.POST['age']
        phone=request.POST['phone']
        address=request.POST['address']
        image=request.FILES.get('img')
        crs=request.POST['course']
        c=Course.objects.get(id=crs)
        if password==cpassword:
            if User.objects.filter(username=user_name).exists():
                messages.info(request,'This username already exists')
                return redirect('signuppage')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'This email already exists')
                return redirect('signuppage')
            elif len(phone)!=10:
                messages.info(request,'Phone Number Should Be 10 Digits')
                return redirect('signuppage')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,password=password,email=email)
                user.save()
                u=User.objects.get(id=user.id)
                crt=Teacher(age=age, phone=phone, user=u, address=address, image=image, course=c)
                crt.save()
                messages.info(request,'Signup Successfull')
                return redirect('signuppage')
        else:
            messages.info(request,'Password doesnot match')
            return redirect('signuppage')
    else:
        return render(request,'signuppage.html')


@login_required(login_url='home')
def userpage(request):
    if 'user' in request.session:
        tchr= Teacher.objects.get(user=request.user)
        return render(request, 'userpage.html', {'t':tchr})
    

def view(request):
    tchr= Teacher.objects.get(user=request.user)
    return render(request, 'view.html', {'t':tchr})

def tchredit(request):
    tchr= Teacher.objects.get(user=request.user)
    crs=Course.objects.all()
    return render(request, 'tchredit.html', {'t':tchr, 'cou':crs})

def edittchr(request,t):
    if request.method == 'POST':
        tchr=Teacher.objects.get(user=t)
        u=User.objects.get(id=t)
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['uname']
        # password=request.POST['pass']
        # cpassword=request.POST['cpass']
        email=request.POST['mail']
        age=request.POST['age']
        phone=request.POST['phone']
        address=request.POST['address']
        
        crs=request.POST['course']
        c=Course.objects.get(id=crs)
        if User.objects.filter(username=username).exclude(id=t).exists():
            messages.info(request,'This username already exists')
            return redirect('tchredit')
        elif User.objects.filter(email=email).exclude(id=t).exists():
            messages.info(request,'This email already exists')
            return redirect('tchredit')
        elif len(phone)!=10:
            messages.info(request,'Phone Number Should Be 10 Digits')
            return redirect('tchredit')
        else:
            if len(request.FILES)!=0:
                if len(tchr.image)>0:
                    os.remove(tchr.image.path)
                tchr.image = request.FILES.get('img')
            u.first_name=fname
            u.last_name=lname
            u.username=username
            u.email=email
            u.save()
            tchr.age=age
            tchr.phone=phone
            tchr.address=address
            tchr.course=c
            tchr.save()
            messages.info(request,'Teacher Updated Successfully')
            return redirect('view')
    else:
        return render(request,'tchredit.html')
