from lib2to3.pgen2 import driver
from pyexpat import model
from statistics import mode
from django.db import models
from datetime import date
from django.utils import timezone
import uuid
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class User(models.Model):
    gender = {
        ('male','male'),
        ('female','female'),
    }
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, unique= True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="male")
    is_driver = models.BooleanField(default=False,null=True,blank=True)
    full_name = models.CharField(max_length=128,null=True,blank=True)
    vehicle_type = models.CharField(max_length=256,null=True,blank=True)
    plate_num = models.CharField(max_length=256,null=True,blank=True)
    max_passenger = models.IntegerField(validators=[
            MinValueValidator(1)
        ],null=True,blank=True)
    special_vehicle_info = models.CharField(max_length=256,null=True,blank=True)
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Order(models.Model):
    # id = uuid.uuid1()
    id = models.BigAutoField(primary_key=True)
    destination = models.CharField(max_length=256)
    arrival_time = models.DateTimeField()
    passenger_number = models.IntegerField(validators=[
            MinValueValidator(1)
        ])
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner',blank=True,null=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='driver')
    is_shared = models.BooleanField(default=False)
    sharer = models.ManyToManyField(User,related_name="sharer",blank=True)
    #open, closed, confirmed
    status_option= {
        ('open','open'),
        ('confirmed','confirmed')
    }
    status = models.CharField(max_length=32, choices=status_option, default="open")
    special_request = models.CharField(max_length=256,blank=True,default='')
    
    special_vehicle_type = models.CharField(max_length=256,blank=True,default='')
    date = models.DateTimeField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
        # + " " + self.date.strftime("%Y-%m-%d") + self.time.strftime("%H:%M")

class UserOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    add_passenger = models.IntegerField(validators=[
            MinValueValidator(1)
        ])

class Meta:
    ordering = ["-c_time"]
    verbose_name = "user"
    verbose_name_plural = "user"

