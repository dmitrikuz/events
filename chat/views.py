from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from .models import Chat

UserModel = get_user_model()


class CreateChatForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=UserModel.objects.all())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_user(self):
        value = self.cleaned_data["user"].pk
        queryset = Chat.objects.filter(
            users=value).filter(users=self.request.user)

        if queryset.exists():
            raise ValidationError("Такой чат уже существует")

        return value

    class Meta:
        model = Chat
        fields = ("user", )


class UserChatsView(LoginRequiredMixin, FormView):
    template_name = "chat/chats.html"
    form_class = CreateChatForm
    success_url = reverse_lazy("chats")

    def get_queryset(self):
        my_chats = Chat.objects.filter(users__pk=self.request.user.pk)
        return my_chats

    def form_valid(self, form):
        selected_user = form.cleaned_data["user"]
        request_user = self.request.user.pk

        new_chat = Chat.objects.create()
        new_chat.users.add(selected_user, request_user)

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["chats"] = self.request.user.chats.all()
        return ctx


class ChatSocketView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "chat/chat.html"
    queryset = Chat.objects.all()

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["chat_id"] = kwargs["object"].id
        ctx["messages"] = kwargs["object"].messages.all()
        return ctx

    def test_func(self):
        chat = self.get_object()
        return self.request.user in chat.users.all()
