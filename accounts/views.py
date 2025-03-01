from calendar import c
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from taggit.models import Tag

from accounts.forms import LoginForm, UserCreationForm
from store.models import Category


# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created Successfully")
            return redirect("accounts:sign_in")
        else:
            messages.error(request, "Some error Occurred!! Please Try again.")
    form = UserCreationForm()
    context = {
        "form": form,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
    }
    return render(request, "accounts/sign_up.html", context=context)


def sign_in(request):
    if request.method == "POST":
        username = LoginForm(request.POST)
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully")
            if user.is_superuser:
                messages.success(request, f"Welcome {user.first_name}")
                return redirect("/admin")
            return redirect("store:home")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("accounts:sign_in")
    form = LoginForm()
    return render(
        request,
        "accounts/sign_in.html",
        context={
            "categories": Category.objects.all(),
            "tags": Tag.objects.all(),
            "form": form,
        },
    )


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("accounts:sign_in")
