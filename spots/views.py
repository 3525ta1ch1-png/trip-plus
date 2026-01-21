from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Spot, Review
from .forms import SpotForm, ReviewForm, WordSearchForm
from django.db.models import Q

def review_list(request):
    reviews = Review.objects.select_related("spot", "user")
    return render(request, "reviews/review_list.html", {"reviews": reviews})

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
    return render(request, "spots/spot_detail.html", {"spot": spot})


def spot_create(request):
    if request.method == "POST":
        form = SpotForm(request.POST)
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
        start_at = form.cleaned_date.get("start_at")
        end_at = form.cleaned_date.get("end_at")
        language = form.cleaned_data.get("language", "").strip()

        if mood:
            spots = spots.filter(mood__icontains=mood)
        if purpose:
            spots = spots.filter(purpose__icontains=purpose)
        if start_at:
            spots = spots.filter(start_at__gte=start_at)
        if end_at:
            spots = spots.filter(end_at__lte=end_at)
        if language:
            spots = spots.filter(language__icontains=language)
        return render(request, "spots/word_search.html", {"form": form, "spots": spots})

def spot_update(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    if request.method == "POST":
        form = SpotForm(request.POST, instance=spot)
        if form.is_valid():
            spot = form.save()
            return redirect("spots:spot_detail", pk=spot.pk)
    else:
        form = SpotForm(instance=spot)

    return render(request, "spots/spot_form.html", {"form": form, "mode": "update", "spot": spot})


def spot_delete(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    if request.method == "POST":
        spot.delete()
        return redirect("spots:spot_list")

    return render(request, "spots/spot_confirm_delete.html", {"spot": spot})

