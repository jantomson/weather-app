import requests
import datetime
import math 

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:    
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')

        context = {'form':form}
        return render(request, 'ilm/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'ilm/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')       

@login_required(login_url='login')
def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = "Tallinn"

    appid = "73a1a511e5b200fef7f3862ca7ca902a"
    URL = "https://api.openweathermap.org/data/2.5/weather"
    PARAMS = {'q':city,'appid':appid,'units':'metric'}
    r = requests.get(url=URL,params=PARAMS)

    res = r.json()
    description = res['weather'][0]['description']
    icon = res['weather'][0]['icon']
    temp = res['main']['temp']
    humidity = res['main']['humidity']
    wind = res['wind']['speed']
    time = datetime.date.today()

    lumi = ['Heavy snow', 'Sleet',"Light shower sleet","Shower sleet","Shower snow","Heavy shower snow"]
    if description == "few clouds":
        description = "vähepilvine"
        icon = "sun"
    if description == "scattered clouds":
        description = "pilvine"
        icon = "clouds"
    if description == "broken clouds":
        description = "pigem pilvine"
        icon = "clouds"
    if description == "overcast clouds":
        description = "lauspilves"
        icon = "clouds"
    elif description == "clear sky":
        description = "selge taevas"
        icon = "sun"
    elif description == "mist":
        description = "udune"
        icon = "mist"
    elif description == "light rain" or description == "light intensity shower rain":
        description = "kerge sadu"
        icon = "rain"
    elif description == "moderate rain":
        description = "keskmine sadu"
        icon = "rain"
    elif description == "heavy intensity rain" or description == "very heavy rain " or description == "extreme rain" or description == "freezing rain" or description == "shower rain" or description == "heavy intensity shower rain" or description == "ragged shower rain":
        description = "tugev sadu"
        icon = "rain"
    elif description in lumi:
        description == "tugev lumesadu"
        icon = "snowflake"
    elif description == "Snow":
        description == "lumesadu"
        icon = "snowflake"
    elif description == "Light snow":
        description == "kerge lumesadu"
        icon = "snowflake"
    elif description == "thunderstorm":
        description == "äiksetorm"
        icon = "lightning"
    elif description == "fog":
        description == "udu"
        icon = "clouds"
    elif description == "mist":
        description == "udu"
        icon = "clouds"
    elif description == "sand":
        description = "liivatorm"
        icon = "sun"

    return render(request,'ilm/ilm.html', {'description':description,'icon':icon,"temp":math.ceil(temp),'time':time,'city':city,'humidity':humidity,'wind':math.ceil(wind)})