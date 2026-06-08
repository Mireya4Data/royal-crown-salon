from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('gallery/', views.gallery, name='gallery'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin-bookings/', views.admin_bookings, name='admin_bookings'),
]