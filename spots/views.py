import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator

from .models import Spot, Review, Favorite
from .forms import SpotForm, ReviewForm, WordSearchForm
from decimal import Decimal

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


from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg

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

    # ✅ 追加：bbox をPython側で作る（テンプレの add を使わない）
    bbox = None
    if spot.latitude is not None and spot.longitude is not None:
        d = Decimal("0.01")
        bbox = {
            "left": spot.longitude - d,
            "bottom": spot.latitude - d,
            "right": spot.longitude + d,
            "top": spot.latitude + d,
        }

    return render(
        request,
        "spots/spot_detail.html",
        {
            "spot": spot,
            "is_favorited": is_favorited,
            "reviews": reviews,
            "reviews_count": reviews_count,
            "avg_rating": avg_rating,
            "bbox": bbox,  # ✅ 追加
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
    spots = Spot.objects.none()

    # ★検索したかどうか（GETが空なら結果は出さない）
    has_query = any([
        request.GET.get("mood"),
        request.GET.get("purpose"),
        request.GET.get("time_axis"),
        request.GET.get("language"),
    ])

    if form.is_valid() and has_query:
        mood = (form.cleaned_data.get("mood") or "").strip()
        purpose = (form.cleaned_data.get("purpose") or "").strip()
        time_axis = (form.cleaned_data.get("time_axis") or "").strip()
        language = (form.cleaned_data.get("language") or "").strip()

        spots = Spot.objects.all()

        if mood:
            spots = spots.filter(mood__icontains=mood)
        if purpose:
            spots = spots.filter(purpose__icontains=purpose)
        if language:
            spots = spots.filter(language__icontains=language)
        if time_axis:
            spots = spots.filter(time_axis__icontains=time_axis)

        # 20件超えの判定（ここも検索時だけ）
        count = spots.count()
        if count > 2:
            return render(request, "spots/word_search_refine.html", {
                "form": form,
                "count": count,
                "candidates": ["温泉系", "カフェ", "自然"],
            })

        # ★ここでだけ annotate する（spots が必ず QuerySet）
        spots = spots.annotate(
            avg_rating=Avg("reviews__rating"),
            reviews_count=Count("reviews"),
        ).order_by("-created_at")

    return render(request, "spots/word_search.html", {"form": form, "spots": spots})

def near_search(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    return render(request, "spots/near_search.html", {"spot": spot})

def near_list(request, pk):
    center = get_object_or_404(Spot, pk=pk)

    # ざっくり：移動時間→半径(km)に変換（後で調整でOK）
    time_map = {"10": 1.0, "30": 3.0, "60": 7.0}
    radius_km = time_map.get(request.GET.get("time") or "", 5.0)  # 指定なしは5km例

    genres = request.GET.getlist("genre")  # 複数チェック
    transport = request.GET.get("transport") or ""
    q = (request.GET.get("q") or "").strip()

    qs = Spot.objects.exclude(pk=center.pk)

    # 例：genreがSpot.genreに入ってる想定（あなたのモデルに合わせて変更）
    if genres:
        qs = qs.filter(genre__in=genres)

    # 例：ワード検索（name/description/addressなど）
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(address__icontains=q)
        )

    # DBで距離計算できない前提で、Python側で距離を付与して絞る
    results = []
    if center.latitude is not None and center.longitude is not None:
        for s in qs:
            if s.latitude is None or s.longitude is None:
                continue
            d = haversine_km(center.latitude, center.longitude, s.latitude, s.longitude)
            if d <= radius_km:
                s.distance_km = round(d, 2)
                results.append(s)

    # 近い順
    results.sort(key=lambda x: x.distance_km)

    context = {
        "center": center,
        "spots": results,
        "radius_km": radius_km,
        "genres": genres,
        "transport": transport,
        "q": q,
    }
    return render(request, "spots/near_list.html", context)


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi/2)**2
         + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2)
    return 2 * R * math.asin(math.sqrt(a))

@login_required
def spot_delete(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    if request.method == "POST":
        spot.delete()
        return redirect("spots:spot_list")

    return render(request, "spots/spot_confirm_delete.html", {"spot": spot})

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

    return render(request, "spots/spot_form.html", {
        "form": form,
        "mode": "update",
        "spot": spot,
    })
