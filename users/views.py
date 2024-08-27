from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("/dashboard")

    form = NewUserForm()
    context = {"form": form}

    return render(request, "register.html", context)
