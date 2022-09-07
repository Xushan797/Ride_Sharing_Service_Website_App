from django.urls import path

from . import views

#app_name = 'login'

urlpatterns = [
    # ex: /user

    #the open_rides list
    path('', views.mainpage, name='mainpage'),

    #edit user information
    path('user_edit/', views.user_edit, name='user_edit'),

    #edit driver information
    path('driver_edit/', views.driver_edit, name='driver_edit'),
    
    #open new ride
    path('open_ride/', views.open_ride, name='open_ride'),

    #my rides list
    path('my_rides_detail/', views.my_rides_detail, name='my_rides_detail'),

    #if choose a ride, see detail information
    path('<int:ride_id>/', views.rides_detail, name='rides_detail'),

    #delete_ride as a owner
    path('<int:ride_id>/delete_ride/', views.delete_ride, name='delete_ride'),

    #delete_ride as a owner
    path('<int:ride_id>/not_ride/', views.not_ride, name='not_ride'),

    #quit_ride as a sharer
    path('<int:ride_id>/quit_ride/', views.quit_ride, name='quit_ride'),
    
    #search ride
    path('search_ride/', views.search_ride, name='search_ride'),

    #search ride
    path('driver_search_ride/', views.driver_search_ride, name='driver_search_ride'),

    #not a driver
    path('not_driver/', views.not_driver, name='not_driver'),


   #not a sharer
    path('not_sharer/', views.not_sharer, name='not_sharer'),

              
]