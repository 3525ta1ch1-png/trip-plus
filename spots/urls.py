from django.urls import path
from . import views

app_name = "spots"

urlpatterns = [
    path("", views.spot_list, name="spot_list"),
    path("<int:pk>/", views.spot_detail, name="spot_detail"),

    path("create/", views.spot_create, name="spot_create"),
    path("<int:pk>/edit/", views.spot_update, name="spot_update"),
    path("<int:pk>/delete/", views.spot_delete, name="spot_delete"),

    path("word-search/", views.word_search, name="word_search"),

    path("reviews/", views.review_list, name="review_list"),
    path("reviews/new/", views.review_pick_spot, name="review_pick_spot"),
    path("<int:spot_id>/reviews/create/", views.review_create, name="review_create"),

    path("<int:pk>/favorite/", views.favorite_toggle, name="favorite_toggle"),
]