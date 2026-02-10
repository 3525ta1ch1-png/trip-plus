


# Create your views here.
import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.db.models import Avg, Count
from spots.models import Spot, Favorite
from .forms import SignupForm, EmailChangeForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        
    return render(request, "accounts/login.html")

def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
            form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})
    
@login_required 
def home(request):
    spots = Spot.objects.all()
    spot = random.choice(list(spots)) if spots.exists() else None
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
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = EmailChangeForm(initial={"email": request.user.email})

    return render(request, "accounts/email_change.html", {"form": form})

@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "accounts/password_change.html", {"form": form})
            
@login_required
def logout_view(request):

    if request.method == "POST":
        logout(request)
        return redirect("accounts:login") 
    return redirect(settings.LOGIN_REDIRECT_URL)    

def portfolio(request):
    return render(request, "accounts/portfolio.html", {
        "proposal_url": "https://docs.google.com/document/d/1Riqf4yRCReR0ypdHptUp1Qnwj_8zE6EjGICylXLNTAs/edit?tab=t.0",
        "design_url": "https://docs.google.com/presentation/d/1VDa8qDI3F5T16SDimrnSULDCvKqjrI-eMCOJvcKhuQE/edit",
        "flow_url": "https://app.diagrams.net/#G1-pSxVzP3ZJNY7yg0DC7Gr4KQYcVul3Nv",
        "er_url": "https://app.diagrams.net/#G1j4-zrC01Le3lSQRQZeEzzgMUGYMzuhDI",
        "app_url": "/home/", 
    })
def landing(request):
    return render(request, "accounts/portfolio.html")