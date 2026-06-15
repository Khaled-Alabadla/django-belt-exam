from django.shortcuts import render, redirect
from django.contrib import messages
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
        # Always process login attempts on POST even if a session exists.
        if request.method == 'POST':
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

            if not email or not password:
                messages.error(request, "Email and password are required.")
                return redirect('login')

            errors, user = User.objects.validate_login(email, password)
            if user:
                request.session['user_id'] = user.id
                return redirect('games:dashboard')

            # Show any validation errors returned by the manager, otherwise a generic message
            if errors:
                for msg in errors.values():
                    messages.error(request, msg)
            else:
                messages.error(request, "Invalid username or password.")
            return redirect('login')

        # GET requests: if already logged in, redirect to dashboard
        if request.session.get('user_id'):
            return redirect('games:dashboard')

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
