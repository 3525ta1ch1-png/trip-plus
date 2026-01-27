from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.portfolio, name="portfolio"),
    path("home/", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("favorites/", views.favorites, name="favorites"),
    path("email-change/", views.email_change, name="email_change"),
    path("password-change/", views.password_change, name="password_change"),
    
]
