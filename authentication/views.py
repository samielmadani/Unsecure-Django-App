import logging

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from authentication.forms import SignUpForm, LoginForm
from authentication.models import UserProfile

logger = logging.getLogger(__name__)


def register_user(request):
    msg = None

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if user_does_not_exist(form) and form.is_valid():
            user = form.save()

            UserProfile(user_id=user.id).save()

            login(request, user)
            return HttpResponseRedirect("/")

        else:
            logger.debug(form.data["username"])
            msg = "Error(s) in form"

    else:
        form = SignUpForm()

    return render(request, 'register.html', {"form": form, "msg": msg})


def login_user(request):
    message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                logger.debug(form.cleaned_data['username'])
                message = "Login failed: Username or password incorrect"

    else:
        form = LoginForm()

    return render(
        request, 'login.html', context={'form': form, 'message': message})


def user_does_not_exist(form):
    input_email = form.data["email"]
    input_username = form.data["username"]
    result = User.objects.filter(email=input_email, username=input_username).count()
    if result > 0:
        form.add_error("email", "Email or username already in use.")
    return result == 0


def logout_user(request):
    response = HttpResponseRedirect("/login/")
    logout(request)
    return response
