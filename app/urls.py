from django.urls import path
from app.views import SignupPage,LoginPage,HomePage,LogoutPage
from django.urls import  path

urlpatterns = [
    path('',SignupPage,name='signup'),
    path('login/',LoginPage,name='login'),
    path('logout/',LogoutPage,name='logout'),
    path('home/',HomePage,name='home'),
    
]
