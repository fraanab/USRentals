from django.utils import timezone
from datetime import datetime, timedelta
from .models import Client, Tour
from django.shortcuts import render, redirect

def payment_verify(request):
	tenants = Client.objects.all()
	now = timezone.now()
	notpaid= Client.objects.filter(paid=False)
	user = []
	for a in notpaid:
		user.append(a.user)

	for a in tenants:
		if a.next_payment < now:
			Client.objects.filter(paid=True, user=a.user).update(paid=False)
			return redirect(request.META['HTTP_REFERER'])
		else:
			print(user, 'checking due payments... 0')
			pass

def tour_verify(request):
	tours = Tour.objects.all()
	now = timezone.now()
	for a in tours:
		if now > a.tour_date:
			# a.tour_date += timedelta(days=1)
			Tour.objects.filter(tour_date=a.tour_date).update(tour_date=a.tour_date+timedelta(days=1))
			print('sending message')
			return redirect(request.META['HTTP_REFERER'])
		else:
			pass


