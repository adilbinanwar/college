from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    coursename=models.CharField(max_length=255)
    fees=models.IntegerField(null=True)


class Student(models.Model):
    studentname=models.CharField(max_length=255)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)    
    address=models.CharField(max_length=255)
    age=models.IntegerField()
    joiningdate=models.DateField()


class Teacher(models.Model):
    age=models.IntegerField(null=True)
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=9)
    image=models.FileField(upload_to='image/',null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)