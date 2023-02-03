from django.shortcuts import render, redirect
from .models import Rental, Tour, Client, Admin
from .models import STATE_CHOICES
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, RentalForm, TourForm, NewTenant
from datetime import datetime, timedelta
from dateutil import relativedelta
from django.utils import timezone
import tzdata
from .utils import payment_verify, tour_verify

def frontpage(request):
	allrentals = Rental.objects.all()
	rentals = Rental.objects.filter(available=True)
	states = []
	for a in STATE_CHOICES:
		states.append(a[0])

	active_category = request.GET.get('category', '')
	if active_category:
		rentals = allrentals.filter(available=True, state=active_category)

	return render(request, 'frontpage.html', {'rentals':rentals, 'states':states, 'allrentals':allrentals})

@login_required
def dashboard(request):
	if request.user.is_superuser:
		tenants = Client.objects.all()
		num_tenants = tenants.count()
		admin_data = Admin.objects.get(pk=1)
		tours = Tour.objects.all()
		num_tours = tours.count()
		due = Client.objects.filter(paid=False)
		dues = due.count()
		now = timezone.now()
		today =  datetime.now()

		payment_verify(request)
		tour_verify(request)

		context = {
			'tenants':tenants,
			'num_tenants':num_tenants,
			'admin_data':admin_data.profit,
			'tours':tours,
			'num_tours':num_tours,
			'dues':dues,
			'due':due
		}
		return render(request, 'admin_dashboard.html', context)
	else:
		tours = Tour.objects.filter(user=request.user)
		rents = Client.objects.filter(user=request.user)

		context = {
			'tours':tours,
			'rents':rents
		}
		return render(request, 'user_dashboard.html', context)

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('/')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form':form})

def rental(request, id):
	rental = Rental.objects.get(id=id)
	tenantForm = NewTenant()
	today = datetime.now()
	admindata = Admin.objects.get(id=1)
	current_profit = admindata.profit


	if request.method=='POST':
		tenantForm = NewTenant(request.POST)
		if tenantForm.is_valid():
			newform = tenantForm.save(commit=False)
			Client.objects.create(
				user=newform.user,
				rental=rental,
				paid=True,
				paid_ammount=rental.rent,
				next_payment=today+timedelta(days=31),
				email=request.user.email
			)
			Rental.objects.filter(id=id).update(available=False)
			Admin.objects.filter(id=1).update(profit=current_profit+rental.rent)
			return redirect('dashboard')
		else:
			print('poop')
			return redirect(request.META['HTTP_REFERER'])
	return render(request, 'rental.html', {'rental':rental, 'tenantForm':tenantForm})

@login_required
def delete_tour(request, id):
	Tour.objects.get(id=id).delete()
	return redirect('dashboard')

@login_required
def new_rental(request):
	if request.method == 'POST':
		form = RentalForm(request.POST, request.FILES)
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.img1 = request.FILES.get('img1')
			new_form.img2 = request.FILES.get('img2')
			new_form.img3 = request.FILES.get('img3')
			new_form.save()
			return redirect(request.META['HTTP_REFERER'])
		else:
			return redirect(request.META['HTTP_REFERER'])

@login_required
def del_rental(request, id):
	if request.user.is_superuser:
		if request.method == 'POST':
			Rental.objects.get(id=id).delete()
			return redirect('/')

@login_required
def new_tour(request, id):
	rental = Rental.objects.get(id=id)
	if request.method == 'POST':
		tour_date = request.POST.get('tour_date')
		move_in_date = request.POST.get('move_in_date')
		message = request.POST.get('message')
		user = request.user
		Tour.objects.create(
			tour_date=tour_date,
			move_in_date=move_in_date,
			message=message,
			user=user,
			rental=rental
			)
		return redirect('dashboard')
	return render(request, 'tour.html', {'rental':rental})

@login_required
def del_client(request, id):
	if request.user.is_superuser:
		thisclient = Client.objects.get(id=id)
		if request.method == 'POST':
			Rental.objects.filter(id=thisclient.rental.id).update(available=True)
			Client.objects.get(id=id).delete()
			return redirect(request.META['HTTP_REFERER'])

@login_required
def deposit(request, id):
	admindata = Admin.objects.get(id=1)
	current_profit = admindata.profit
	rental = Rental.objects.get(id=id)
	today = datetime.now()

	if request.method=='POST':
		Client.objects.filter(user=request.user, rental=id).update(paid=True, next_payment=today+timedelta(days=31))
		Admin.objects.filter(id=1).update(profit=current_profit+rental.rent)
		return redirect(request.META['HTTP_REFERER'])