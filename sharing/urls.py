from django.urls import path
from .views import *

urlpatterns = [
    path('user/signup/', userSignUp, name='User_Sign_Up'),
    path('user/givefood/', giveFood, name='Give_Food'),
    path('user/takefood/', regTaker, name='Register_Taker'),
    path('user/numFood/<option>/<int:piece>/', numFoodAvailable, name='Number_Of_Food_Available')
]