from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Rental, Tour, Client

class SignUpForm(UserCreationForm):
	# first_name = forms.CharField(max_length=50, required=True)
	# last_name = forms.CharField(max_length=50, required=True)
	email = forms.EmailField(max_length=255, required=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2',]

class RentalForm(forms.ModelForm):
	class Meta:
		model = Rental
		fields = '__all__'

class TourForm(forms.ModelForm):
	class Meta:
		model = Tour
		fields = ['tour_date', 'move_in_date', 'message']
		widgets = {
			'tour_date':forms.DateTimeInput(attrs = {'type':'date'}),
			'move_in_date':forms.DateTimeInput(attrs = {'type':'time','min':'08:00','max':'19:00'})
		}

class NewTenant(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['user']