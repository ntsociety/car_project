from django.contrib import messages, auth
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from contacts.models import Contact

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Vous êtes mainenant connecter !')
            return redirect('dashboard')
        else:
            messages.error(request, 'identifiant ou mot de passe incorrect')
            return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                    messages.error(request, 'nom d\'utilisateur existe déjà')
                    return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email existe déjà')
                    return redirect('register')
                else:
                    user = User.objects.create(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    auth.login(request, user)
                    messages.success(request, 'Inscription reçue avec succes!, Vous êtes mainenant connecter !')
                    user.save()
                    return redirect('dashboard')
                    # messages.succes(request, 'Inscription reçue avec succes!')
                    # return redirect('register')
        else:
            messages.error(request, 'le mot de passe ne correspond pas')
            return redirect('register')
        # messages.error(request, 'this is the error message')
        
    else:
        return render(request, 'accounts/register.html')
@login_required(login_url = 'login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data = {
        'inquiries': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Vous êtes déconnecter avec succès !')
        return redirect('home')
    return render('logout')