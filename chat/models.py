from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Chat(models.Model):

    @property
    def participants(self):
        return self.users.all()

    @property
    def last_message(self):
        if (msg := self.messages.last()) is not None:
            return str(msg)
        return "..."


class Message(models.Model):

    from_user = models.ForeignKey(
        to=UserModel,
        on_delete=models.SET_NULL,
        related_name="messages",
        null=True
    )
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}: {}".format(
            self.timestamp.strftime("%d.%m %H:%M"),
            self.from_user.email,
            self.text
        )
