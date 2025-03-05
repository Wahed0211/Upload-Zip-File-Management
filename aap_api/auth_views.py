from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Get user by email
            user = User.objects.get(email=email)
            # Authenticate using username (since Django uses username for auth)
            user = authenticate(username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': f"{reverse('aap_api:item-list')}?login_success=true"
                    })
                return redirect(f"{reverse('aap_api:item-list')}?login_success=true")
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid email or password.'
                    })
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'No account found with this email.'
                })
            messages.error(request, 'No account found with this email.')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Login error: {str(e)}'
                })
            messages.error(request, f'Login error: {str(e)}')
            
    return render(request, 'aap_api/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'aap_api/register.html')

        try:
            # Create user with email as username
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1
            )
            messages.success(request, 'Registration successful! Please login.')
            return redirect('aap_api:login')
        except IntegrityError:
            messages.error(request, 'Email already exists!')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'aap_api/register.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('aap_api:login'))
