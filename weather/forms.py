from django import forms
from .models import  City


class CityWeatherForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'type':'text',
        'name':'seher',
        'class':'form-control',
        'placeholder':'Seher Adi Girin'
    }))
    
    class Meta:
        model = City
        fields = ['name']