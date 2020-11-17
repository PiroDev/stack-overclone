from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')

def registration_view(request):
    return render(request, 'registration.html')

def profile_settings_view(request):
    return render(request, 'profile_settings.html')