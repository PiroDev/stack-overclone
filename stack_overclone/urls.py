from django.urls import path, include
import users.urls, questions.urls
from django.contrib import admin
from django.shortcuts import redirect
from .error_views import *

handler404 = page_not_found_view

urlpatterns = [
    path('', lambda request: redirect('questions/', permanent=True)),
    path('admin/', admin.site.urls),
    path('user/', include(users.urls)),
    path('questions/', include(questions.urls))
]
