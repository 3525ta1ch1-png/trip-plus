from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("favorites/", views.favorites, name="favorites"),
    path("signup/", views.signup, name="signup"),
    path("email-change/", views.email_change, name="email_change"),
    path("password-change/", views.password_change, name="password_change"),
    
]
