from core.forms import RentalForm

def rentalform(request):
	rental_form = RentalForm()
	return{
		'rental_form':rental_form
	}