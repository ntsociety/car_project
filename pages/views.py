from pickle import TRUE
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from cars.models import Car
from pages.models import Team
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured=True)
    all_cars = Car.objects.order_by('-created_date')
    model_search = Car.objects.values_list('model', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    data = {
        'teams' : teams,
        'featured_cars': featured_cars,
        'all_cars': all_cars,
        'model_search': model_search,
        'year_search': year_search,
        'city_search': city_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'pages/home.html', data)

def about(request):
    teams = Team.objects.all()
    data = {
        'teams' : teams
    }
    return render(request, 'pages/about.html', data)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']
        
        # Subject = subject
        # message = message
        email_from = settings.EMAIL_HOST_USER
        # recipient_list = [admin_email]
        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        email_subject = 'vous avez un nouveau message du site car dealer ' + subject
        message_body = 'Name:' + name + '. Email:' + email + '. Phone:' + phone + '. Message:' + message 
        send_mail(
            email_subject,
            message_body,
            email_from,
            [admin_email],
            fail_silently=False,
        )
        messages.success(request, 'merci pour votre contact, votre requêtte a été prise en charge!')
        
        return redirect('contact')
    return render(request, 'pages/contact.html')

def services(request):
    return render(request, 'pages/services.html')