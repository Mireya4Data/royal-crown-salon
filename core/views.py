from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Service, Staff, Booking
from datetime import datetime, timedelta, date


def home(request):
    return render(request, 'home.html')


def services(request):
    services_list = Service.objects.all()
    return render(request, 'services.html', {'services': services_list})


def gallery(request):
    return render(request, 'gallery.html')


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "🎉 Welcome to Royal Crown! Your account has been created successfully.")
            return redirect('home')
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            return render(request, 'login.html', {'form': form, 'login_error': True})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def my_bookings(request):
    today = date.today()
    Booking.objects.filter(date__lt=today, status='pending').update(status='completed')
    bookings = Booking.objects.filter(customer=request.user).order_by('-date', '-start_time')
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking has been cancelled successfully.")
    else:
        messages.error(request, "Only pending bookings can be cancelled.")
    return redirect('my_bookings')


@login_required(login_url='login')
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    staff_list = Staff.objects.all()

    if request.method == 'POST':
        date_str = request.POST.get('date')
        start_time_str = request.POST.get('start_time')
        staff_id = request.POST.get('staff_id')

        try:
            staff = Staff.objects.get(id=staff_id) if staff_id else Staff.objects.first()

            if not staff:
                messages.error(request, "No staff available.")
                return redirect('book_service', service_id=service.id)

            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=service.duration)).time()

            overlapping = Booking.objects.filter(
                staff=staff,
                date=date_str,
                status__in=['pending', 'confirmed']
            ).filter(
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if overlapping:
                messages.error(request, "❌ This time slot is already taken. Please choose another time.")
                return redirect('book_service', service_id=service.id)

            Booking.objects.create(
                customer=request.user,
                service=service,
                staff=staff,
                date=date_str,
                start_time=start_time,
                end_time=end_time,
                status='pending'
            )

            messages.success(request, f"✅ Booking confirmed with {staff} on {date_str}!")
            return redirect('my_bookings')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'book.html', {
        'service': service,
        'staff_list': staff_list,
    })


@staff_member_required(login_url='login')
def admin_bookings(request):
    all_bookings = Booking.objects.all().order_by('-date', '-start_time')
    total = all_bookings.count()
    pending = all_bookings.filter(status='pending').count()
    confirmed = all_bookings.filter(status='confirmed').count()
    completed = all_bookings.filter(status='completed').count()
    cancelled = all_bookings.filter(status='cancelled').count()
    return render(request, 'admin_bookings.html', {
        'all_bookings': all_bookings,
        'total': total,
        'pending': pending,
        'confirmed': confirmed,
        'completed': completed,
        'cancelled': cancelled,
    })