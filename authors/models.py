from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Author(AbstractUser, models.Model):
    # ABSTRACTUSER MODEL
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    name = models.CharField(default="name", null=False, max_length=50)
    description = models.TextField(default="", null=True, max_length=250)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username


class Book(models.Model):
    name = models.CharField(default="name", null=False, max_length=50)
    description = models.TextField(default="", null=True, max_length=250)
    made = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
