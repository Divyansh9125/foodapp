from django.urls import path
from .views import *

urlpatterns = [
    path('user/signup/', userSignUp, name='User_Sign_Up'),
    path('user/givefood/', giveFood, name='Give_Food'),
]