from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import User

def register_view(request):
     if request.method == 'POST':
            errors = User.objects.validate_registration(request.POST)
            if not errors:
                user = User.objects.create_user(request.POST)
                request.session['user_id'] = user.id
                return redirect('/games')
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
     return render(request, "accounts/register.html")


def login_view(request):
        if request.method == 'POST':
                email = request.POST.get('email', '')
                password = request.POST.get('password', '')
                errors, user = User.objects.validate_login(email, password)
                if user:
                    request.session['user_id'] = user.id
                    return redirect('/')
                messages.error(request, "Invalid username or password.")
                return redirect('/games')
                
        return render(request, 'accounts/login.html')

def logout_view(request):
    # Manual session-based logout
    request.session.flush()
    return redirect('login')

def profile(request, pk):
      user = User.objects.get(pk=pk)
      return render(request, "accounts/profile.html", {
            'user': user
      })
