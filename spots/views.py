from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator

from .models import Spot, Review, Favorite
from .forms import SpotForm, ReviewForm, WordSearchForm

@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        raise Http404
    
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "クチコミを更新しました！ ")
            return redirect("spots:spot_detail", pk=review.spot.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/review_form.html", {"form": form, "spot": review.spot, "mode": "update"})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        raise Http404
    
    if request.method == "POST":
        spot_pk = review.spot.pk
        review.delete()
        messages.success(request, "クチコミを削除しました。 ")
        return redirect("spots:spot_detail", pk=spot_pk)
    
    return render(request, "reviews/review_confirm_delete.html", {"review": review})

@login_required
def review_list(request):
    sort = request.GET.get("sort", "new")
    spot_id = request.GET.get("spot")

    reviews = Review.objects.select_related("spot", "user")

    spot = None
    if spot_id:
        reviews = reviews.filter(spot_id=spot_id)
        spot = get_object_or_404(Spot, pk=spot_id)

    if sort == "high":
        reviews = reviews.order_by("-rating", "-created_at")
    elif sort == "low":
        reviews = reviews.order_by("rating", "-created_at")
    else:
        reviews = reviews.order_by("-created_at")

    paginator = Paginator(reviews, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "reviews/review_list.html", {
        "page_obj": page_obj,
        "reviews": reviews,
        "sort": sort,
        "spot_id": spot_id,
        "spot": spot,
    })

@login_required
def review_pick_spot(request):
    spots = Spot.objects.order_by("-created_at")
    return render(request, "reviews/review_pick_spot.html", {"spots": spots})

@login_required
def favorite_toggle(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    if request.method != "POST":
        return redirect("spots:spot_detail", pk=spot.pk)
    
    fav, created = Favorite.objects.get_or_create(user=request.user, spot=spot)

    if not created:
        fav.delete()
    return redirect("spots:spot_detail", pk=spot.pk)

@login_required
def favorite_list(request):
    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related("spot")
        .order_by("-created_at")
    )
    return render(request, "spots/favorite_list.html", {"favorites": favorites})

@login_required
def review_create(request, spot_id):
    spot = get_object_or_404(Spot, pk=spot_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.spot = spot
            review.user = request.user
            review.save()
            messages.success(request, "クチコミを投稿しました！")

            return redirect("spots:spot_detail", pk=spot.pk)
    else:
        form = ReviewForm()

    return render(request, "reviews/review_form.html", {"form": form, "spot": spot})

def spot_list(request):
    q = request.GET.get("q", "").strip()
    lang = request.GET.get("lang", "").strip()

    spots = Spot.objects.order_by("-created_at")

    if q:
        spots = spots.filter(Q(name__icontains=q) | Q(address__icontains=q))

    if lang:
        spots = spots.filter(language=lang)

    languages = (
        Spot.objects.exclude(language="")
        .values_list("language", flat=True)
        .distinct()
        .order_by("language")
    )

    return render(
        request,
        "spots/spot_list.html",
        {"spots": spots, "q": q, "lang": lang, "languages": languages},
    )


def spot_detail(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, spot=spot).exists()

    reviews_all = spot.reviews.all()

    reviews = (
        spot.reviews.select_related("user")
        .order_by("-rating", "-created_at")[:3]
    )
    
    reviews_count = reviews_all.count()
    avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"]
    
    return render(
        request,
        "spots/spot_detail.html", 
        {
            "spot": spot,                                          
            "is_favorited": is_favorited,
            "reviews": reviews,
            "reviews_count": reviews_count,
            "avg_rating": avg_rating,
        },
    )

@login_required
def spot_create(request):
    if request.method == "POST":
        form = SpotForm(request.POST, request.FILES)
        if form.is_valid():
            spot = form.save()
            return redirect("spots:spot_detail", pk=spot.pk)
    else:
        form = SpotForm()

    return render(request, "spots/spot_form.html", {"form": form, "mode": "create"})


def word_search(request):
    form = WordSearchForm(request.GET or None)
    spots = Spot.objects.order_by("-created_at")

    if form.is_valid():
        mood = form.cleaned_data.get("mood", "").strip()
        purpose = form.cleaned_data.get("purpose", "").strip()
        start_at = form.cleaned_data.get("start_at")
        end_at = form.cleaned_data.get("end_at")
        language = form.cleaned_data.get("language", "").strip()

        if mood:
            spots = spots.filter(mood__icontains=mood)
        if purpose:
            spots = spots.filter(purpose__icontains=purpose)
        if language:
            spots = spots.filter(language__icontains=language)
        if start_at and end_at:
            spots = spots.filter(start_at__lte=end_at, end_at__gte=start_at)
        elif start_at:
            spots = spots.filter(end_at__gte=start_at)
        elif end_at:
            spots = spots.filter(start_at__lte=end_at)

    spots = spots.annotate(
        avg_rating=Avg("reviews__rating"),
        reviews_count=Count("reviews")
    ).order_by("-created_at")
            
    return render(request, "spots/word_search.html", {"form": form, "spots": spots})

@login_required
def spot_update(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    if request.method == "POST":
        form = SpotForm(request.POST, request.FILES, instance=spot)
        if form.is_valid():
            spot = form.save()
            return redirect("spots:spot_detail", pk=spot.pk)
    else:
        form = SpotForm(instance=spot)

    return render(request, "spots/spot_form.html", {"form": form, "mode": "update", "spot": spot})

@login_required
def spot_delete(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    if request.method == "POST":
        spot.delete()
        return redirect("spots:spot_list")

    return render(request, "spots/spot_confirm_delete.html", {"spot": spot})

