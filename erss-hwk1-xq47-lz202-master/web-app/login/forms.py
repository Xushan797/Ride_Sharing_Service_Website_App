from datetime import datetime
from django.utils import timezone
from email.policy import default
from hashlib import sha1
from lib2to3.pgen2 import driver
#from tkinter.tix import Form
from tokenize import Special
from django import forms
from captcha.fields import CaptchaField
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Order,User, UserOrder

class UserForm(forms.Form):
    username = forms.CharField(label="user name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))
    captcha = CaptchaField(label='verification code')

class RegisterForm(forms.Form):
    gender = (
        ('male', "male"),
        ('female', "female"),
    )
    username = forms.CharField(label="user name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="password again", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email address", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='gender', choices=gender)
    captcha = CaptchaField(label='verification code')
    isDriver = forms.BooleanField(initial = False, required=False)

class DriverForm(forms.Form):
    driver_name = forms.CharField(label="driver name", max_length=128,initial = "", widget=forms.TextInput(attrs={'class': 'form-control'}))
    vehicle_type = forms.CharField(label="vehicle type", max_length=128,initial = "", widget=forms.TextInput(attrs={'class': 'form-control'}))
    plate_num = forms.CharField(label="license plate number", max_length=128,initial = "", widget=forms.TextInput(attrs={'class': 'form-control'}))
    max_passenger = forms.IntegerField(validators=[
            MinValueValidator(1),MaxValueValidator(10)
        ],label="max passenger number",initial = 1,widget=forms.TextInput(attrs={'class': 'form-control'}))
    special_info = forms.CharField(label="special information",max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    special_info.required = False
class UserEditForm(forms.Form):
    gender = (
        ('male', "male"),
        ('female', "female"),
    )
    password1 = forms.CharField(label="password", max_length=256,initial = "", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="password again", max_length=256,initial = "", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email address",initial = "", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='gender', choices=gender)

class OwnerRideForm(forms.Form):

    destination = forms.CharField(label="destination", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    arrival_time = forms.DateTimeField(label="arrival time, Format: '%m/%d/%y %H:%M AM/PM', input like this: '10/25/06 14:30 AM/PM'",
    input_formats = ['%m/%d/%y %H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%m/%d/%y %H:%M'))
    passenger_number = forms.IntegerField(label="passenger number",validators=[
            MinValueValidator(1), MaxValueValidator(10)
        ])
    CHOICES = [('True', 'True'), ('False', 'False')]
    is_shared = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    special_request = forms.CharField(label="special request", max_length=128, required = False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    special_vehicle_type = forms.CharField(label="special vehicle type", max_length=128,required = False, widget=forms.TextInput(attrs={'class': 'form-control'}))

class DetailsForm(forms.ModelForm):
    class Meta:
        model = Order
        # widgets = {
        #     'sharer': forms.SelectMultiple(attrs={'readonly': 'True', 'readonly': 'True'})
        # }
        fields = "__all__"
        #exclude = ['sharer']
    add_passenger_number = forms.IntegerField(label='add passenger number')
    character = (
        ('driver', "driver"),
        ('sharer', "sharer"),
        ('no', "no"),
    )
    character = forms.ChoiceField(label='to be driver/sharer', choices=character)
    def __init__(self, order_model, is_owner, is_driver, is_sharer, *args, **kwargs):
        super(DetailsForm, self).__init__(*args,**kwargs)
        
        self.fields["sharer"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["sharer"].help_text = ""
        self.fields["sharer"].queryset = order_model.sharer.all()

        self.fields['destination'].required = False
        self.fields['arrival_time'].required = False
        self.fields['owner'].required = False
        self.fields['driver'].required = False
        self.fields['passenger_number'].required = False
        self.fields['is_shared'].required = False
        self.fields['sharer'].required = False
        #self.fields['add_passenger_number'].required = False
        self.fields['status'].required = False
        self.fields['date'].required = False
        self.fields['time'].required = False
        self.fields['character'].required = False
        self.fields['special_request'].required = False
        self.fields['completed'].required = False
        self.fields['special_vehicle_type'].required = False

        if order_model.status == "open":
            
            if is_owner:
                # self.fields['destination'].widget.attrs['readonly']  = 'readonly'
                # self.fields['arrival_time'].widget.attrs['readonly']  = 'readonly'
                self.fields['owner'].widget.attrs['disabled']  = 'disabled'
                self.fields['driver'].widget.attrs['disabled']  = 'disabled'
                self.fields['passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['is_shared'].widget.attrs['disabled']  = 'disabled'
                self.fields['sharer'].widget.attrs['disabled'] = 'disabled'
                # self.fields['add_passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['status'].widget.attrs['disabled']  = 'disabled'
                self.fields['date'].widget.attrs['readonly']  = 'readonly'
                self.fields['time'].widget.attrs['readonly']  = 'readonly'
                self.fields['character'].widget.attrs['disabled']  = 'disabled'
                self.fields['completed'].widget.attrs['disabled']  = 'disabled'
                # self.fields['special_request'].widget.attrs['readonly']  = 'readonly'
                #self.fields['special_vehicle_type'].widget.attrs['readonly']  = 'readonly'
                
            elif is_sharer:
                self.fields['destination'].widget.attrs['readonly']  = 'readonly'
                self.fields['arrival_time'].widget.attrs['readonly']  = 'readonly'
                self.fields['owner'].widget.attrs['disabled']  = 'disabled'
                self.fields['driver'].widget.attrs['disabled']  = 'disabled'
                self.fields['passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['is_shared'].widget.attrs['disabled']  = 'disabled'
                self.fields['sharer'].widget.attrs['disabled'] = 'disabled'
                # self.fields['add_passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['status'].widget.attrs['disabled']  = 'disabled'
                self.fields['date'].widget.attrs['readonly']  = 'readonly'
                self.fields['time'].widget.attrs['readonly']  = 'readonly'
                self.fields['character'].widget.attrs['disabled']  = 'disabled'
                self.fields['completed'].widget.attrs['disabled']  = 'disabled'
                self.fields['special_request'].widget.attrs['readonly']  = 'readonly'
                self.fields['special_vehicle_type'].widget.attrs['readonly']  = 'readonly'      
                
            else:
                # 路人可以选择成为driver/sharer
                self.fields['destination'].widget.attrs['readonly']  = 'readonly'
                self.fields['arrival_time'].widget.attrs['readonly']  = 'readonly'
                self.fields['owner'].widget.attrs['disabled']  = 'disabled'
                self.fields['driver'].widget.attrs['disabled']  = 'disabled'
                self.fields['passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['is_shared'].widget.attrs['disabled']  = 'disabled'
                self.fields['sharer'].widget.attrs['disabled'] = 'disabled'
                self.fields['add_passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['status'].widget.attrs['disabled']  = 'disabled'
                self.fields['date'].widget.attrs['readonly']  = 'readonly'
                self.fields['time'].widget.attrs['readonly']  = 'readonly'
                # self.fields['character'].widget.attrs['disabled']  = 'disabled'
                self.fields['completed'].widget.attrs['disabled']  = 'disabled'
                self.fields['special_request'].widget.attrs['readonly']  = 'readonly'
                self.fields['special_vehicle_type'].widget.attrs['readonly']  = 'readonly'

        elif order_model.status == "confirmed":
            if is_driver and not order_model.completed:
                # 司机可以标记订单状态为完成
                self.fields['destination'].widget.attrs['readonly']  = 'readonly'
                self.fields['arrival_time'].widget.attrs['readonly']  = 'readonly'
                self.fields['owner'].widget.attrs['disabled']  = 'disabled'
                self.fields['driver'].widget.attrs['disabled']  = 'disabled'
                self.fields['passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['is_shared'].widget.attrs['disabled']  = 'disabled'
                self.fields['sharer'].widget.attrs['disabled'] = 'disabled'
                self.fields['add_passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['status'].widget.attrs['disabled']  = 'disabled'
                self.fields['date'].widget.attrs['readonly']  = 'readonly'
                self.fields['time'].widget.attrs['readonly']  = 'readonly'
                self.fields['character'].widget.attrs['disabled']  = 'disabled'
                # self.fields['completed'].widget.attrs['disabled']  = 'disabled'
                self.fields['special_request'].widget.attrs['readonly']  = 'readonly'
                self.fields['special_vehicle_type'].widget.attrs['readonly']  = 'readonly'
            else:
                self.fields['destination'].widget.attrs['readonly']  = 'readonly'
                self.fields['arrival_time'].widget.attrs['readonly']  = 'readonly'
                self.fields['owner'].widget.attrs['disabled']  = 'disabled'
                self.fields['driver'].widget.attrs['disabled']  = 'disabled'
                self.fields['passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['is_shared'].widget.attrs['disabled']  = 'disabled'
                self.fields['sharer'].widget.attrs['disabled'] = 'disabled'
                self.fields['add_passenger_number'].widget.attrs['readonly']  = 'readonly'
                self.fields['status'].widget.attrs['disabled']  = 'disabled'
                self.fields['date'].widget.attrs['readonly']  = 'readonly'
                self.fields['time'].widget.attrs['readonly']  = 'readonly'
                self.fields['character'].widget.attrs['disabled']  = 'disabled'
                self.fields['completed'].widget.attrs['disabled']  = 'disabled'
                self.fields['special_request'].widget.attrs['readonly']  = 'readonly'
                self.fields['special_vehicle_type'].widget.attrs['readonly']  = 'readonly'
        
        else:
            self.fields['destination'].widget.attrs['readonly']  = 'readonly'
            self.fields['arrival_time'].widget.attrs['readonly']  = 'readonly'
            self.fields['owner'].widget.attrs['disabled']  = 'disabled'
            self.fields['driver'].widget.attrs['disabled']  = 'disabled'
            self.fields['passenger_number'].widget.attrs['readonly']  = 'readonly'
            self.fields['is_shared'].widget.attrs['disabled']  = 'disabled'
            self.fields['sharer'].widget.attrs['disabled'] = 'disabled'
            self.fields['add_passenger_number'].widget.attrs['readonly']  = 'readonly'
            self.fields['status'].widget.attrs['disabled']  = 'disabled'
            self.fields['date'].widget.attrs['readonly']  = 'readonly'
            self.fields['time'].widget.attrs['readonly']  = 'readonly'
            self.fields['character'].widget.attrs['disabled']  = 'disabled'
            self.fields['completed'].widget.attrs['disabled']  = 'disabled'
            self.fields['special_request'].widget.attrs['readonly']  = 'readonly'
            self.fields['special_vehicle_type'].widget.attrs['readonly']  = 'readonly'

class SharerPassengerForm(forms.ModelForm):
    class Meta:
        model = UserOrder
        fields = ['add_passenger']
    def __init__(self,*args, **kwargs):
        super(DetailsForm, self).__init__(*args,**kwargs)


class SearchForm(forms.Form):
    destination = forms.CharField(label="destination", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    arrival_time_early = forms.DateTimeField(label="early arrival time,Format: '%m/%d/%y %H:%M', input like this: '10/25/06 14:30 AM/PM'", 
    input_formats = ['%m/%d/%y %H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%m/%d/%y %H:%M'))
    arrival_time_late = forms.DateTimeField(label="late arrival time,Format: '%m/%d/%y %H:%M', input like this: '10/25/06 14:30 AM/PM'",
     input_formats = ['%m/%d/%y %H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%m/%d/%y %H:%M'))
    open_seat = forms.IntegerField(validators=[
            MinValueValidator(1),MaxValueValidator(10)
        ],label="open_seat number",initial = 1,widget=forms.TextInput(attrs={'class': 'form-control'}))


class Driver_SearchForm(forms.Form):
    max_passenger = forms.IntegerField(validators=[
            MinValueValidator(1)
        ],label="max passenger number",initial = 1,widget=forms.TextInput(attrs={'class': 'form-control'}))