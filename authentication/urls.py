from django.urls import path
from .views import LoginView, LogoutView
from .google_oauth import GoogleLoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('google/login/', GoogleLoginView.as_view(), name='google-login'),
]
