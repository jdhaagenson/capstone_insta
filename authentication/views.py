from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from instauser.models import InstaUser
from .forms import LoginForm, AddUserForm
from django.views.generic import TemplateView


class CreateUser(TemplateView):
    def get(self, request):
        form = AddUserForm
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            InstaUser.objects.create_user(
                username=data.get("username"),
                display_name=data.get("display_name"),
                password=data.get("password"),
                bio=data.get("bio"),
                profile_pic=data.get("profile_pic"),
            )

            return HttpResponseRedirect(reverse("homepage"))


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("homepage"))
                )

    form = LoginForm
    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))