from django import forms
from restaurants.models import Burger, Restaurant

class BurgerForm(forms.ModelForm):
   class Meta:
       model = Burger
       fields = '__all__'

class RestaurantForm(forms.ModelForm):
   class Meta:
       model = Restaurant
       fields = '__all__'