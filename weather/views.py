from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import  *
from django.db.models import F, Q
from django.contrib import messages
import requests

# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f68d1b5b546294cd6ef3fa159a2fe650'

    if request.method == 'POST':
        form = CityWeatherForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city = City.objects.filter(name__icontains=new_city).exists()
            
            if city:
                messages.add_message(request,messages.INFO,'Bele Bir Seher Movcuddur')
            
            else:#eger bele bir seher movcud deyilse
                response = requests.get(url.format(new_city)).json()
                
                if response['cod'] == 200:
                    form.save()

    else:
        form = CityWeatherForm()
        
        
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        response = requests.get(url.format(city)).json()

        fahrenheit = response['main']['temp']
        results = 5/9 * (fahrenheit - 32)
        celcius = round(results, 2)

        cityweather = {
            'city': city.name,
            'temperature': celcius,
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
            'timezone': response['timezone'],
            'speed': response['wind']['speed'],
            'humidity': response['main']['humidity'],
            'pressure': response['main']['pressure']
        }
        
    
        weather_data.append(cityweather)
        uzunlug = len(weather_data)
        


    context = {
        'weather_data': weather_data,
        'form':form,
        'response':response,
        'uzunlug':uzunlug
    }

    return render(request, 'weather/index.html', context)



def delete_city(request,name):
    city = get_object_or_404(City,name=name)
    print(city)
    city.delete()
    return redirect('index')
