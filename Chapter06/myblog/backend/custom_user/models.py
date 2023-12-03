from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


######
# Uncomment CustomUserManager and CustomUser code to use custom user model in Django.
# Please note if you are testing this code You need to do the following steps:
# * Delete all migrations from custom_user app.
# * Create a new database and run migrations again.
# If you use it with existing database you will get errors.
# There are ways to integrate it with existing database but that is out of scope of this book.
######


# class CustomUserManager(BaseUserManager):
#     """
#     Used for updating default behaviors Django provides
#     """
#
#     def create_user(self, phone_no, password, **kwargs):
#         # implement create user logic
#         user = self.model(phone_no=phone_no, **kwargs)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, phone_no, password, **kwargs):
#         # creates superuser.
#         user = self.create_user(phone_no, password, **kwargs)
#         return user
#
#
# class CustomUser(AbstractUser):
#     username = None
#     phone_no = models.CharField(unique=True, max_length=20)
#     city = models.CharField(max_length=40)
#     USERNAME_FIELD = "phone_no"
#     objects = CustomUserManager()

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='user_profile', on_delete=models.CASCADE)
    phone_no = models.CharField(unique=True, max_length=20)
    city = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"