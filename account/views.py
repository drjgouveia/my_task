from django.shortcuts import render

# Create your views here.
from django.contrib import messages
import django.contrib.auth as auth
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from account.forms import RegisterForm
import logging

logger = logging.getLogger(__name__)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("task:list")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="account/login.html", context={"login_form": form})


def register(request):
    try:
        if request.method == "POST":
            form = RegisterForm(request.POST)

            if form.is_valid():
                user = form.save()
                auth.login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("task:list")
            else:
                logger.error(form.errors)

            messages.error(request, "Unsuccessful registration. Invalid information.")

        form = RegisterForm()
        return render(request, "account/register.html", context={"register_form": form})
    except Exception:
        messages.error(request, "An error occurred!")
        return redirect("task:list")


def logout(request):
    auth.logout(request)
    return redirect("account:login")
