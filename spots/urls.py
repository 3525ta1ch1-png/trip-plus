from django.urls import path
from . import views

app_name = "spots"

urlpatterns = [
    path("", views.spot_list, name="spot_list"),
    path("word-search/", views.word_search, name="word_search"),
    path("create/", views.spot_create, name="spot_create"),
    path("<int:pk>/", views.spot_detail, name="spot_detail"),
    path("<int:pk>/edit/", views.spot_update, name="spot_update"),
    path("<int:pk>/delete/", views.spot_delete, name="spot_delete"),
    path("reviews/", views.review_list, name="review_list"),
    path("<int:spot_id>/reviews/create/", views.review_create, name="review_create"),
]
