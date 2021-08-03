
from django.contrib import admin
from django.urls import path, include
from . import views
app_name="payment"
urlpatterns = [
    path('', views.donation_view, name="donate"),
    path('payments/create',views.create_payment,name='create_payment'),
    path('payments/invoice/<pk>',views.track_invoice,name='track_payment'),
    path('payments/recieve',views.recieve_payment,name='recieve_payment'),
    
]
