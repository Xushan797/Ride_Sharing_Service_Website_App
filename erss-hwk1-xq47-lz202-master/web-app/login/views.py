# from asyncio.windows_events import NULL
from curses.ascii import NUL
from email import message
from telnetlib import STATUS
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import datetime
import pytz
from django.utils import timezone
from .models import Order,User, UserOrder
from django.urls import reverse
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse
# Create your views here.
from django.core.mail import send_mail
from project import settings
import hashlib

def convert_local_timezone(time_in):
    local = pytz.timezone('US/Eastern')
    local_dt = local.localize(time_in, is_dst=None)
    time_utc = local_dt.astimezone(pytz.utc)
    return time_utc

def convert_timezone(time_in):
    time_utc = time_in.replace(tzinfo=pytz.timezone('UTC'))
    time_local = time_utc.astimezone(pytz.timezone('US/Eastern'))
    return time_local

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
    

def welcome(request):
    return render(request, "login/welcome.html")

def mainpage(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if not request.session.get('is_login', None):
        return redirect('/login/')
    orders = Order.objects.filter(status = 'open')
    # 指定渲染模板并传递数据
    return render(request, "login/mainpage.html", locals())

def login(request):
    # login_form = forms.UserForm()
    # if request.session.get('is_login', None):  # 不允许重复登录
    #     return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = 'please check the input information!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message = 'user not exist!'
                return render(request, 'login/login.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                
                orders = Order.objects.all()
                # 指定渲染模板并传递数据
                # return render(request, 'login/mainpage.html', locals())
                return redirect(reverse("mainpage"))
            else:
                message = 'password not correct!'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())



def register(request):
    # if request.session.get('is_login', None):
    #     return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "please check the input such as email format!"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = 'password is different!'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = 'user already exist!'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = 'this email is already registered!'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password =  password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")

def user_edit(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        user_edit_form = forms.UserEditForm(request.POST)
        message = "please check the input!"
        if user_edit_form.is_valid():
            password1 = user_edit_form.cleaned_data.get('password1')
            password2 = user_edit_form.cleaned_data.get('password2')
            email = user_edit_form.cleaned_data.get('email')
            sex = user_edit_form.cleaned_data.get('sex')
            if password1 != password2:
                message = 'password is different!'
                return render(request, 'login/user_edit.html', locals())
            edit_user = get_object_or_404(User, pk=user_id)
            edit_user.password =  password1
            edit_user.email = email
            edit_user.sex = sex
            edit_user.save()
            message = 'successfully save the edit!'
    # 指定渲染模板并传递数据
            # return render(request, "login/mainpage.html", {"orders": orders, "user_id" : user_id})
            return redirect(reverse("mainpage"))
        return render(request, 'login/user_edit.html',{'user_id': user_id})
    user_edit_form = forms.UserEditForm()
    return render(request, 'login/user_edit.html',locals())

def driver_edit(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        driver_form = forms.DriverForm(request.POST)
        message = "please check the input!"
        if driver_form.is_valid():
            driver_name = driver_form.cleaned_data.get('driver_name')
            vehicle_type =driver_form .cleaned_data.get('vehicle_type')
            plate_num = driver_form.cleaned_data.get('plate_num')
            max_passenger = driver_form.cleaned_data.get('max_passenger')
            special_vehicle_info = driver_form.cleaned_data.get('special_info')
            if max_passenger < 1 or max_passenger > 10:
                message = 'please enter passenger number between 1 ~ 10!'
                return render(request, 'login/driver_edit.html', locals())
            user.full_name = driver_name
            user.vehicle_type =  vehicle_type
            user.plate_num =  plate_num
            user.max_passenger =  max_passenger
            user.special_vehicle_info =  special_vehicle_info
            user.is_driver = True
            user.save()
            message = "successfully save the edit!"
            orders = Order.objects.all()
    # 指定渲染模板并传递数据
            # return render(request, "login/mainpage.html", {"orders": orders, "user_id" : user_id})
            return render(request, 'login/driver_edit.html',locals())
        return render(request, 'login/driver_edit.html',locals())
    driver_form = forms.DriverForm()
    return render(request, 'login/driver_edit.html',locals())

def open_ride(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        open_ride_form = forms.OwnerRideForm(request.POST)
        message = "please check the input!"
        if open_ride_form.is_valid():
            
            destination = open_ride_form.cleaned_data.get('destination')
            arrival_time =open_ride_form.cleaned_data.get('arrival_time')
            if arrival_time < convert_timezone(timezone.now()) :
                message = "input time is invalid!"
                return render(request, 'login/open_ride.html', locals())
            passenger_number = open_ride_form.cleaned_data.get('passenger_number')
            if passenger_number > 10 or passenger_number < 1:
                message = "input time is invalid!"
                return render(request, 'login/open_ride.html', locals())
            is_shared = open_ride_form.cleaned_data.get('is_shared')
            special_request = open_ride_form.cleaned_data.get('special_request')
            special_vehicle_type = open_ride_form.cleaned_data.get('special_vehicle_type')
            order = Order()
            order.destination  = destination 
            order.arrival_time =  arrival_time
            order.passenger_number =  passenger_number
            order.is_shared  =  is_shared 
            order.owner = user
            order.special_request = special_request
            order.special_vehicle_type = special_vehicle_type
            order.save()
            sharer_info = UserOrder.objects.get_or_create(user=user.id, order=order.id, defaults={'user': user, 'order':order, 'add_passenger':order.passenger_number})[0]
            orders = Order.objects.all()
    # 指定渲染模板并传递数据
            # return render(request, "login/mainpage.html", {"orders": orders, "user_id" : user_id})
            return redirect(reverse("mainpage"))
        return render(request, 'login/open_ride.html',locals())
    open_ride_form = forms.OwnerRideForm()
    return render(request, 'login/open_ride.html', locals())

def my_rides_detail(request):
    user_id = request.session.get('user_id')
    owner_order = Order.objects.filter(owner = user_id)
    driver_order = Order.objects.filter(driver = user_id)
    sharer_order = Order.objects.filter(sharer = user_id)
    # sharer_order = Order.objects.filter(completed = False)
    return render(request, 'login/my_rides_detail.html',locals())

def rides_detail(request, ride_id):
    # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKkK")
    user_id = request.session.get('user_id')

    order = get_object_or_404(Order, pk=ride_id)
    user = get_object_or_404(User, pk=user_id)
    
    is_owner = order in Order.objects.filter(owner=user.id)
    is_driver = order in Order.objects.filter(driver=user.id)
    is_sharer = order in Order.objects.filter(sharer=user.id)
    
    original_add_passanger_number = 0
    sharer_info = UserOrder.objects.get_or_create(user=user.id, order=order.id, defaults={'user': user, 'order':order, 'add_passenger':0})[0]
    character_info = "no"
    if is_driver:
        character_info = "driver"
    elif is_sharer:
        character_info = "sharer"
    
    original_add_passanger_number = sharer_info.add_passenger
    
    if request.method == 'POST':
        #message = "please check the input!"
        # sharer_form = forms.SharerForm(request.POST)
        
        ride_detail_form = forms.DetailsForm(data=request.POST, order_model=order, is_owner=is_owner, is_driver=is_driver, is_sharer=is_sharer)
        print(ride_detail_form.errors)
        if ride_detail_form.is_valid():
            print('valid------------------------------------------')
            if order.status == "open":
                if is_owner:
                    destination = ride_detail_form.cleaned_data.get('destination')
                    arrival_time =ride_detail_form.cleaned_data.get('arrival_time')
                    special_request = ride_detail_form.cleaned_data.get('special_request')
                    add_passenger_number = ride_detail_form.cleaned_data.get('add_passenger_number')
                    if order.passenger_number - original_add_passanger_number + add_passenger_number > 10:
                        return render(request, 'login/not_sharer.html',locals())
                    if order.destination != destination or order.arrival_time !=  arrival_time:
                        email_title = 'your order has been cancelled!'
                        email_body = 'your order has been cancelled, ride_ id is:' + str(order.id)
                        for each_sharer in order.sharer.all():
                            email = each_sharer.email
                            send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
                        order.sharer.clear()

                    order.destination  = destination 
                    order.arrival_time =  arrival_time
                    order.special_request = special_request
                    order.passenger_number = order.passenger_number - original_add_passanger_number + add_passenger_number

                elif is_sharer:
                    add_passenger_number = ride_detail_form.cleaned_data.get('add_passenger_number')
                    if order.passenger_number - original_add_passanger_number + add_passenger_number > 10:
                        return render(request, 'login/not_sharer.html',locals())
                    order.passenger_number = order.passenger_number - original_add_passanger_number + add_passenger_number
                    sharer_info.add_passenger = add_passenger_number
                    sharer_info.save()

                else:
                    character = ride_detail_form.cleaned_data.get('character')
                    if character == 'sharer':
                        if not order.is_shared:
                            message = "order cannot share"
                            return render(request, 'login/not_sharer.html',locals())
                        if order.passenger_number >= 10:
                            return render(request, 'login/not_sharer.html',locals())
                        order.sharer.add(user)
                    elif character == 'driver':
                        if not user.is_driver:
                            message = "please register as a driver!"
                            return render(request, 'login/not_driver.html',locals())
                        if order.special_vehicle_type:
                            print(user.special_vehicle_info)
                            if not user.vehicle_type:
                                message = "vehicle type is not match"
                                print('1')
                                return render(request, 'login/not_driver.html',locals())
                            if order.special_vehicle_type.strip().lower() not in user.vehicle_type.lower():
                                print('2')
                                message = "vehicle type is not match"
                                return render(request, 'login/not_driver.html',locals())
                        if order.passenger_number > user.max_passenger:
                            message = "passenger number is not match"
                            return render(request, 'login/not_driver.html',locals())
                        if order.special_request:
                            if not user.special_vehicle_info:
                                message = "special info is not match"
                                return render(request, 'login/not_driver.html',locals())  
                            if order.special_request.strip().lower() not in user.special_vehicle_info.lower():
                                message = "special info is not match"
                                return render(request, 'login/not_driver.html',locals())  
                                
                            
                        order.completed = ride_detail_form.cleaned_data.get('completed')
                        order.driver = user
                        order.status = 'confirmed'
                        email_title = 'your order has been confirmed!'
                        email_body = 'your order has been confirmed, ride_ id is:' + str(order.id)
                        email = order.owner.email  #对方的邮箱
                        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
                        for each_sharer in order.sharer.all():
                            email = each_sharer.email
                            send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
            
            elif order.status == "confirmed" and not order.completed:
                if is_driver:
                    completed = ride_detail_form.cleaned_data.get('completed')
                    order.completed = completed

            # destination = ride_detail_form.cleaned_data.get('destination')
            # arrival_time =ride_detail_form.cleaned_data.get('arrival_time')
            # passenger_number = ride_detail_form.cleaned_data.get('passenger_number')
            # is_shared = ride_detail_form.cleaned_data.get('is_shared')
            # special_request = ride_detail_form.cleaned_data.get('special_request')
            # special_vehicle_type = ride_detail_form.cleaned_data.get('special_vehicle_type')
            # character = ride_detail_form.cleaned_data.get('character')
            # add_passenger_number = ride_detail_form.cleaned_data.get('add_passenger_number')
            # completed = ride_detail_form.cleaned_data.get('completed')
            # status = ride_detail_form.cleaned_data.get('status')
            # sharer_info.add_passenger = add_passenger_number
            # sharer_info.save()

            # order = get_object_or_404(Order, pk=ride_id)

            # order.status = status
            # order.destination  = destination 
            # order.arrival_time =  arrival_time
            # order.passenger_number = passenger_number
            # order.is_shared  =  is_shared 
            # order.completed = completed
            # order.special_request = special_request
            # order.special_vehicle_type = special_vehicle_type
            # order.passenger_number = order.passenger_number - original_add_passanger_number + add_passenger_number

            # if character == 'sharer':
            #     order.sharer.add(user)
            # elif character == 'driver':
            #     order.driver = user
            #     order.status = 'confirmed'
            #     email_title = '邮件标题'
            #     email_body = '邮件内容'
            #     email = order.owner.email  #对方的邮箱
            #     send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
            #     for each_sharer in order.sharer.all():
            #         email = each_sharer.email
            #         send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
            order.save()
    # 指定渲染模板并传递数据
            message = "save the change!"
            
            # return render(request, 'login/rides_detail.html',locals())
            print(get_object_or_404(Order, pk=ride_id) is None)
            return redirect(reverse('rides_detail', args=(ride_id,)))
        return redirect(reverse('rides_detail', args=(ride_id,)))
        
    ride_detail_form = forms.DetailsForm(order_model=order, is_owner=is_owner, is_driver=is_driver, is_sharer=is_sharer,
        initial = {'id': order.id, 'destination':order.destination,
    'arrival_time':order.arrival_time,
    'passenger_number':order.passenger_number, 'add_passenger_number':sharer_info.add_passenger,
    'owner':order.owner, 'driver':order.driver, 'is_shared':order.is_shared, 
    'sharer':order.sharer.all(), 'completed':order.completed,
    'status':order.status,  'special_request':order.special_request, 
    'special_vehicle_type':order.special_vehicle_type,  'date':order.date, 'time' :order.time, 'character':character_info})
    return render(request, 'login/rides_detail.html',locals())

def search_result(request,order_result):
    user_id = request.session.get('user_id')
    return render(request, 'login/search_result.html',{{order_result:order_result}})


def not_sharer(request):
    user_id = request.session.get('user_id')
    return render(request, 'login/not_sharer.html')

def delete_ride(request,ride_id):
    user_id = request.session.get('user_id')
    order = get_object_or_404(Order, pk=ride_id)
    if order.status == 'confirmed':
        return render(request, 'login/not_ride.html')
    user = get_object_or_404(User, pk=user_id)
    order.delete()
    return render(request, 'login/delete_ride.html')

def not_driver(request,ride_id):
    return render(request, 'login/not_driver.html')

def quit_ride(request,ride_id):
    user_id = request.session.get('user_id')
    order = get_object_or_404(Order, pk=ride_id)
    if order.status == 'confirmed':
        return render(request, 'login/not_ride.html')
    user = get_object_or_404(User, pk=user_id)
    order.sharer.remove(user)
    return render(request, 'login/quit_ride.html')

def not_ride(request,ride_id):
    user_id = request.session.get('user_id')
    order = get_object_or_404(Order, pk=ride_id)
    user = get_object_or_404(User, pk=user_id)
    return redirect(reverse('rides_detail', args=(ride_id,)))

def search_ride(request):

    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        search_form = forms.SearchForm(request.POST)
        message = "The results are shown!"
        # print(search_form.errors())
        if search_form.is_valid():
            destination = search_form.cleaned_data.get('destination')
            arrival_time_early = search_form.cleaned_data.get('arrival_time_early')
            arrival_time_late = search_form.cleaned_data.get('arrival_time_late')
            required_seat = 10 - search_form.cleaned_data.get('open_seat')
            order_result = models.Order.objects.filter(status = 'open')
            order_result = order_result.filter(destination = destination)
            order_result = order_result.filter(arrival_time__lte = arrival_time_late)
            order_result = order_result.filter(arrival_time__gte = arrival_time_early)
            order_result = order_result.filter(passenger_number__lte = required_seat)
            
    # 指定渲染模板并传递数据
            # return render(request, "login/mainpage.html", {"orders": orders, "user_id" : user_id})
            return render(request, 'login/search_ride.html',locals())
    search_form = forms.SearchForm()
    return render(request, 'login/search_ride.html',locals())

def driver_search_ride(request):

    user_id = request.session.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        driver_search_form = forms.Driver_SearchForm(request.POST)
        message = "The results are shown!"
        # print(search_form.errors())
        print("11111111111")
        if driver_search_form.is_valid():
            max_passenger = driver_search_form.cleaned_data.get('max_passenger')
            
            if max_passenger > user.max_passenger:
                
                message = "Please input an max passenger number your car can accommodate!"
                return render(request, 'login/driver_search_ride.html',locals())
            print("max passenger ", max_passenger)
            order_result = models.Order.objects.filter(passenger_number__lte = max_passenger)
            order_result = order_result.filter(status = 'open')
            print(order_result)
            # print("1 ", order_result)
            if  user.vehicle_type:
                order_result1 = order_result.filter(special_vehicle_type = "")
                order_result = order_result.filter(special_vehicle_type = user.vehicle_type)
                order_result = order_result1 | order_result
                print("2 ", order_result)

            if not user.special_vehicle_info:
                order_result = order_result.filter(special_request = "")
            else:
                order_result2 = order_result.filter(special_request = "")
                order_result = order_result.filter(special_request = user.special_vehicle_info)
                order_result = order_result2 | order_result
                print("3 ", order_result)
    # 指定渲染模板并传递数据
            # return render(request, "login/mainpage.html", {"orders": orders, "user_id" : user_id})
            return render(request, 'login/driver_search_ride.html',locals())
    driver_search_form = forms.Driver_SearchForm()
    return render(request, 'login/driver_search_ride.html',locals())