from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "spots"

urlpatterns = [
    # Spot
    path("", views.spot_list, name="spot_list"),
    path("create/", views.spot_create, name="spot_create"),
    path("<int:pk>/", views.spot_detail, name="spot_detail"),
    path("<int:pk>/edit/", views.spot_update, name="spot_update"),
    path("<int:pk>/delete/", views.spot_delete, name="spot_delete"),

    # Word search
    path("word-search/", views.word_search, name="word_search"),
    path("word-search/results/", views.word_search_results, name="word_search_results"),

    # Near search
    path("<int:pk>/near/search/", views.near_search, name="near_search"),
    path("<int:pk>/near/", views.near_list, name="near_list"),

    # Reviews
    path("review-spots/", views.review_spot_list, name="review_spot_list"),  # ←クチコミしたスポット一覧
    path("reviews/", views.review_list, name="review_list"),                 # ←クチコミ一覧（spotで絞れる）
    path("reviews/new/", views.review_pick_spot, name="review_pick_spot"),
    path("reviews/new/<int:spot_id>/", views.review_create, name="review_create"),
    path("reviews/<int:pk>/edit/", views.review_update, name="review_update"),
    path("reviews/<int:pk>/delete/", views.review_delete, name="review_delete"),

    # Favorites
    path("favorites/", views.favorite_list, name="favorite_list"),
    path("<int:pk>/favorite/", views.favorite_toggle, name="favorite_toggle"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)