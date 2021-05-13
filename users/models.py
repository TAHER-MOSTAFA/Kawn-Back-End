from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MemberManager(UserManager):
    def _create_user(self, full_name, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, full_name, email=None, password=None, username=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(full_name, email, password, **extra_fields)

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)


class Member(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="media/profile_pics", default="1.jpg")
    cover = models.ImageField(upload_to="media/profile_pics", default="1.jpg")

    first_name = None
    last_name = None
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = MemberManager()

    def natural_key(self):
        return dict(email=self.email)

    def __str__(self):
        return self.full_name


class Circle(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    icon = models.ImageField(upload_to="media/circlepics")
    cover = models.ImageField(upload_to="media/circlepics")
