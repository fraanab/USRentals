from django.contrib import admin
from .models import Rental, Tour, Client, Admin

admin.site.register(Rental)
admin.site.register(Tour)
admin.site.register(Client)
admin.site.register(Admin)