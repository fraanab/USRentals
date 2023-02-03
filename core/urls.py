from django.urls import path, include
from .views import frontpage, signup, dashboard, rental, delete_tour, new_rental, del_rental, new_tour, del_client, deposit
from django.contrib.auth import views
from django.contrib import admin

urlpatterns = [
	path('', frontpage, name='frontpage'),
	path('signup/', signup, name='signup'),
	path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('dashboard/', dashboard, name='dashboard'),
	path('rental/<int:id>/', rental, name='rental'),
	path('delete/<int:id>/', delete_tour, name='delete_tour'),
	path('new_rental/', new_rental, name='new_rental'),
	path('del_rental/<int:id>/', del_rental, name='del_rental'),
	path('new_tour/<int:id>/', new_tour, name='new_tour'),
	path('del_client/<int:id>/', del_client, name='del_client'),
	path('payment/<int:id>/', deposit, name='deposit')
]