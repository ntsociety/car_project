from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from contacts.models import Contact
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def inquiry(request):
    if request.method == 'POST':
        car_id = request.POST['car_id']
        car_title = request.POST['car_title']
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        customer_need = request.POST['customer_need']
        city = request.POST['city']
        state = request.POST['state']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(car_id=car_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'Vous avez déjà envyer une demande pour cette voiture.')
                return redirect('/cars/'+car_id)
        
        contact = Contact(car_id=car_id, car_title=car_title, user_id=user_id, first_name=first_name,
                          last_name=last_name, customer_need=customer_need, city=city, state=state, email=email, phone=phone, message=message)
        
        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        Subject = 'Nouvelle demande de voiture'
        message = 'Vous avez une nouvelle demande de voiture ' + car_title + '. svp connectez-vous à votre tableau de bord admin pour plus  info.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [admin_email]
        send_mail(
            Subject,
            message,
            email_from,
            recipient_list,
            fail_silently=False,
        )
        # send_mail(
        #     'Nouvelle demande de voiture',
        #     'Vous avez une nouvelle demande de voiture ' + car_title + '. svp connectez-vous à votre tableau de bord admin pour plus  info.',
        #     'sylvestreanani228@gmail.com',
        #     [admin_email],
        #     fail_silently=False
             
        # )
        
        contact.save()
        messages.success(request, 'merci pour votre contact, votre requêtte a été prise en charge!')
        return redirect('/cars/'+car_id)