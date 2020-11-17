from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', registration_view, name='signup'),
    path('profile/', profile_settings_view, name='profile')
]