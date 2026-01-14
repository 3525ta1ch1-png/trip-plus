

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from spots.models import Spot, Favorite



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        
    return render(request, "accounts/login.html")

@login_required 
def home(request):
    spot = Spot.objects.order_by("?").first()
    return render(request, "accounts/home.html", {"spot": spot})

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("spot")
    spots = [f.spot for f in favorites]
    return render(request, "accounts/favorites.html", {"spots": spots})

@login_required
def reviews(request):
    return HttpResponse("クチコミ一覧（ダミー）")

@login_required
def review_post(request):
    return HttpResponse("クチコミ投稿（ダミー）")

@login_required
def spot_create(request):
    return HttpResponse("スポット登録（ダミー）")

@login_required
def email_change(request):
    return HttpResponse("メールアドレス変更（ダミー）")

@login_required
def password_change(request):
    return HttpResponse("パスワード変更（ダミー）")

@login_required
def spot_detail(request, pk):
    return HttpResponse(f"スポット詳細（ダミー） id={pk}")

@login_required
def word_search(request):
    return HttpResponse("ワード検索ページ（ダミー）")


@login_required
def logout_view(request):

    if request.method == "POST":
        logout(request)
        return redirect("login")  # ログイン画面へ戻す
    return redirect("home")      # GETで来たらホームへ
