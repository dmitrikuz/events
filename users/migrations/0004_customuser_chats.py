# Generated by Django 5.0.3 on 2024-03-11 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
        ("users", "0003_alter_customuser_organization"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="chats",
            field=models.ManyToManyField(related_name="users", to="chat.chat"),
        ),
    ]
