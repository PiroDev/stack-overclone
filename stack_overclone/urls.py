from django.urls import path
from django.contrib import admin
from .error_views import *

handler404 = page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),
]
