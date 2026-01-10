from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("word-search/", views.word_search, name="word_search"),
    path("spots/<int:pk>/", views.spot_detail, name="spot_detail"),
    path("favorites/", views.favorites, name="favorites"),
    path("reviews/", views.reviews, name="reviews"),
    path("review-post/", views.review_post, name="review_post"),
    path("spots/create/", views.spot_create, name="spot_create"),
    path("email-change/", views.email_change, name="email_change"),
    path("password-change/", views.password_change, name="password_change"),
    
]
