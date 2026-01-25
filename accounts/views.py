

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from spots.models import Spot, Favorite
from .forms import SignupForm, EmailChangeForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        
    return render(request, "accounts/login.html")

def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_vaild():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            login(request, user)
            return redirect("home")
        else:
            form = SignupForm()
        return render(request, "accounts/signup.html", {"form": form})
    
@login_required 
def home(request):
    spot = Spot.objects.order_by("-created_at").first()
    return render(request, "accounts/home.html", {"spot": spot})

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("spot").order_by("-created_at")
    spots = [f.spot for f in favorites]
    return render(request, "accounts/favorites.html", {"spots": spots})

@login_required
def reviews(request):
   return redirect("spots:review_list")

@login_required
def review_post(request):
    return redirect("spots:review_pick_spot")

@login_required
def email_change(request):
    if request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EmailChangeForm(instence=request.user)

    return render(request, "accounts/email_change.html", {"form": form})

@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("home")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "accounts/password_change.html", {"form": form})
            
@login_required
def logout_view(request):

    if request.method == "POST":
        logout(request)
        return redirect("login")  # ログイン画面へ戻す
    return redirect("home")      # GETで来たらホームへ
