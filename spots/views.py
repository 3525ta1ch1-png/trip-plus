import math
import re
from collections import Counter
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, Max
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Spot, Review, Favorite
from .forms import SpotForm, ReviewForm, WordSearchForm


SEP = "/"


def _split_keywords(s: str):
    if not s:
        return []
    parts = [p.strip() for p in s.split(SEP) if p.strip()]
    out = []
    for p in parts:
        out += [x.strip() for x in re.split(r"[,\s、/]+", p) if x.strip()]
    return out


def _build_candidates(spots_qs, exclude_words=None, top_n=3):
    exclude_words = set([w for w in (exclude_words or []) if w])

    counter = Counter()
    for s in spots_qs.values("mood", "purpose", "time_axis", "language"):
        for field in ("mood", "purpose", "time_axis", "language"):
            for kw in _split_keywords(s.get(field)):
                if kw in exclude_words:
                    continue
                if len(kw) <= 1:
                    continue
                counter[kw] += 1

    return [w for w, _ in counter.most_common(top_n)]


# ------------------------
# Review（クチコミ） CRUD
# ------------------------

@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        raise Http404

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "クチコミを更新しました！")
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
        messages.success(request, "クチコミを削除しました。")
        return redirect("spots:spot_detail", pk=spot_pk)

    return render(request, "reviews/review_confirm_delete.html", {"review": review})


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


@login_required
def review_pick_spot(request):
    spots = Spot.objects.all().order_by("-id")
    return render(request, "reviews/review_pick_spot.html", {"spots": spots})


# -----------------------------------------
# ✅ ヘッダー「クチコミ一覧」= クチコミがあるスポット一覧
# -----------------------------------------

@login_required
def review_spot_list(request):
    """
    自分がクチコミしたスポット一覧（グリッド）
    1ページ8件。最新クチコミ順。
    """

    qs = (
        Spot.objects
        .filter(reviews__user=request.user)  # ← ★ここ重要
        .annotate(
            reviews_count=Count("reviews", distinct=True),
            last_reviewed_at=Max("reviews__created_at"),
        )
        .distinct()
        .order_by("-last_reviewed_at")
    )

    paginator = Paginator(qs, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "spots/reviewed_spot_list.html", {
        "page_obj": page_obj,
        "spots": page_obj,
    })

@login_required
def review_list(request):
    """
    Review（クチコミ）一覧。spot=ID があればそのスポットに絞る。
    常に新着順。
    """
    spot_id = request.GET.get("spot")

    reviews = Review.objects.select_related("spot", "user")

    spot = None
    avg_rating = None
    reviews_count = 0

    if spot_id:
        spot = get_object_or_404(Spot, pk=spot_id)
        reviews = reviews.filter(spot_id=spot_id)

        reviews_count = reviews.count()
        avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"]

    reviews = reviews.order_by("-created_at")

    paginator = Paginator(reviews, 8)  # 1ページ8件
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "reviews/review_list.html", {
        "page_obj": page_obj,
        "reviews": page_obj,
        "spot_id": spot_id,
        "spot": spot,
        "avg_rating": avg_rating,
        "reviews_count": reviews_count,
    })

@login_required
def favorite_toggle(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    if request.method != "POST":
        return redirect("spots:spot_detail", pk=spot.pk)

    fav, created = Favorite.objects.get_or_create(user=request.user, spot=spot)
    if not created:
        fav.delete()

    # ✅ 元ページへ戻す（一覧で解除しても一覧に戻る）
    return redirect(request.META.get("HTTP_REFERER", reverse("spots:spot_detail", args=[spot.pk])))


@login_required
def favorite_list(request):
    qs = (
        Favorite.objects
        .filter(user=request.user)
        .select_related("spot")
        .order_by("-created_at")
    )

    paginator = Paginator(qs, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "spots/favorite_list.html", {
        "page_obj": page_obj,
        "favorites": page_obj,
    })


# ------------------------
# Spot（スポット）
# ------------------------

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
        .order_by("-created_at")[:3]  # ✅ 最新3件（新着順）
    )

    reviews_count = reviews_all.count()
    avg_rating = reviews_all.aggregate(avg=Avg("rating"))["avg"]

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
            "bbox": bbox,
        },
    )


@login_required
def spot_create(request):
    if request.method == "POST":
        form = SpotForm(request.POST, request.FILES)
        if form.is_valid():
            spot = form.save(commit=False)
            spot.created_by = request.user
            spot.save()
            form.save_m2m()
            return redirect("spots:spot_detail", pk=spot.pk)
    else:
        form = SpotForm()

    return render(request, "spots/spot_form.html", {"form": form, "mode": "create"})


@login_required
def spot_delete(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    if spot.created_by != request.user:
        messages.error(request, "登録ユーザーのみ編集可能です。")
        return redirect("spots:spot_detail", pk=spot.pk)
    
    if request.method == "POST":
        spot.delete()
        messages.success(request, "削除しました。")
        return redirect("spots:spot_list")

    return render(request, "spots/spot_confirm_delete.html", {"spot": spot})


@login_required
def spot_update(request, pk):
    spot = get_object_or_404(Spot, pk=pk)

    if spot.created_by !=request.user:
        messages.error(request, "登録ユーザーのみ編集可能です。")
        return redirect("spots:spot_detail", pk=spot.pk)
    
    if request.method == "POST":
        form = SpotForm(request.POST, request.FILES, instance=spot)
        if form.is_valid():
            form.save()
            messages.success(request, "更新しました。")
            return redirect("spots:spot_detail", pk=spot.pk)
        else:
            form = SpotForm(instance=spot)

        return render(request, "spots/spot_form.html", {"form": form, "mode": "update", "spot": spot})

# ------------------------
# Word Search（ワード検索）
# ------------------------

def word_search(request):
    form = WordSearchForm(request.GET or None)
    return render(request, "spots/word_search.html", {"form": form})


def _guess_refine_target(word: str) -> str:
    w = (word or "").strip()
    time_keys = ["日帰り", "朝活", "夜", "雨", "週末", "平日", "午前", "午後", "夕方", "年末年始"]
    purpose_keys = ["温泉", "カフェ", "食べ歩き", "体験", "学習", "自然", "神社", "夜景", "動物", "美術館", "水族館"]

    if any(k in w for k in time_keys):
        return "time_axis"
    if any(k in w for k in purpose_keys):
        return "purpose"
    return "language"


def word_search_results(request):
    form = WordSearchForm(request.GET or None)

    candidate = (request.GET.get("candidate") or "").strip()
    free_word = (request.GET.get("free_word") or "").strip()
    refine_word = candidate or free_word

    has_query = any([
        (request.GET.get("mood") or "").strip(),
        (request.GET.get("purpose") or "").strip(),
        (request.GET.get("time_axis") or "").strip(),
        (request.GET.get("language") or "").strip(),
        refine_word,
    ])
    if not has_query:
        return redirect("spots:word_search")

    spots = Spot.objects.all()

    if form.is_valid():
        mood = (form.cleaned_data.get("mood") or "").strip()
        purpose = (form.cleaned_data.get("purpose") or "").strip()
        time_axis = (form.cleaned_data.get("time_axis") or "").strip()
        language = (form.cleaned_data.get("language") or "").strip()

        if mood:
            spots = spots.filter(mood__icontains=mood)
        if purpose:
            spots = spots.filter(purpose__icontains=purpose)
        if time_axis:
            spots = spots.filter(time_axis__icontains=time_axis)
        if language:
            spots = spots.filter(language__icontains=language)

        if refine_word:
            spots = spots.filter(
                Q(mood__icontains=refine_word) |
                Q(purpose__icontains=refine_word) |
                Q(time_axis__icontains=refine_word) |
                Q(language__icontains=refine_word) |
                Q(name__icontains=refine_word) |
                Q(address__icontains=refine_word) |
                Q(description__icontains=refine_word)
            )

        count = spots.count()

        if count >= 20 and not refine_word:
            search_word = language or mood or purpose or time_axis
            candidates = _build_candidates(
                spots_qs=spots,
                exclude_words=[search_word],
                top_n=3
            )

            return render(request, "spots/word_search_refine.html", {
                "form": form,
                "count": count,
                "search_word": search_word,
                "candidates": candidates,
            })

        spots = spots.annotate(
            avg_rating=Avg("reviews__rating"),
            reviews_count=Count("reviews", distinct=True),
        ).order_by("-created_at")

        paginator = Paginator(spots, 8)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "spots/word_search_results.html", {
            "form": form,
            "spots": page_obj,
            "page_obj": page_obj,
            "count": count,
            "refine_word": refine_word,
            "querystring": request.GET.urlencode(),
        })

    return redirect("spots:word_search")


# ------------------------
# Near Search（近く検索）
# ------------------------

def near_search(request, pk):
    spot = get_object_or_404(Spot, pk=pk)
    return render(request, "spots/near_search.html", {"spot": spot})


def near_list(request, pk):
    center = get_object_or_404(Spot, pk=pk)

    time_map = {"10": 1.0, "30": 3.0, "60": 7.0}
    radius_km = time_map.get(request.GET.get("time") or "", 5.0)

    q = (request.GET.get("q") or "").strip()

    qs = Spot.objects.exclude(pk=center.pk)

    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(address__icontains=q)
        )

    results = []
    if center.latitude is not None and center.longitude is not None:
        for s in qs:
            if s.latitude is None or s.longitude is None:
                continue
            d = haversine_km(
                float(center.latitude), float(center.longitude),
                float(s.latitude), float(s.longitude)
            )
            if d <= radius_km:
                s.distance_km = round(d, 2)
                results.append(s)

    results.sort(key=lambda x: x.distance_km)

    context = {
        "center": center,
        "spots": results,
        "radius_km": radius_km,
        "q": q,
    }
    return render(request, "spots/near_list.html", context)


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))