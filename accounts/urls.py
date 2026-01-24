from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("favorites/", views.favorites, name="favorites"),
    path("reviews/", views.reviews, name="reviews"),
    path("review-post/", views.review_post, name="review_post"),
    path("email-change/", views.email_change, name="email_change"),
    path("password-change/", views.password_change, name="password_change"),
    
]
