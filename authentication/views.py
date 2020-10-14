from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from instauser.models import InstaUser
from .forms import LoginForm, AddUserForm
from django.views.generic import TemplateView, CreateView


class CreateUser(CreateView):
    form_class = AddUserForm
    template_name = "signup.html"
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            img = form.cleaned_data.get('profile_pic')
            display_name = form.cleaned_data.get('display_name')
            bio = form.cleaned_data.get('bio')
            obj = InstaUser.objects.create_user(
                username=username,
                display_name=display_name,
                password=password,
                bio=bio,
                profile_pic=img,
            )
            obj.save()

            return HttpResponseRedirect(reverse('homepage'))
        return render(request, self.template_name, {'form': form})


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