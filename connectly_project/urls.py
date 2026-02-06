from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
    path('posts/', include('posts.urls')),
    path('tasks/', include('tasks.urls')),
    path('auth/', include('authentication.urls')),
    path('', lambda request: redirect('api-auth/login/')),  # redirect root → login
]
