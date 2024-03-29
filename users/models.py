from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        BaseUserManager, PermissionsMixin)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# from chat.models import Chat
# from main.models import Organization


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Email", unique=True)
    organization = models.ForeignKey(
        to="main.Organization",
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = CustomUserManager()
    chats = models.ManyToManyField(to="chat.Chat", related_name="users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        abstract = False
