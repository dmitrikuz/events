from django.contrib.auth.views import redirect_to_login
from django.forms import ModelForm
from django.urls import reverse
from django.views.generic import CreateView

from .models import CustomUser


class SignupForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password", "organization")

    def save(self, commit=True):
        return CustomUser.objects.create_user(**self.cleaned_data)


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        form.save()
        return redirect_to_login(next=reverse("chats"))
