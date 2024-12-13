from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Rohit(models.Manager):
    def address(self):
        return self.all().only('user','title')
    def full_address(self):
        return self.all().defer('country')
class Address(models.Model):
    objects = Rohit()
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    code = models.CharField(max_length=20) 

class Customer(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='customer/profile/img')
    age = models.IntegerField()
    contact_details = models.CharField(max_length=13)
    gender = models.CharField(choices=[('M','Male'),('F','Female'),('O','Other')] , max_length=1)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





