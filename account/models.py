import datetime
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


class Node(MPTTModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, null=True)
    is_right = models.BooleanField(default=0)
    total_point = models.IntegerField(default=0)
    left_point = models.IntegerField(default=0)
    right_point = models.IntegerField(default=0)
    user_parent = models.ForeignKey(User, null=True, blank=True, related_name='user_children', on_delete=models.DO_NOTHING)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Nodes"

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=50)
    point = models.IntegerField(default=0)
    price_som = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name


class Bonus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price_som = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True, blank=True)
    type = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, null=True)
    last_name = models.CharField(max_length=60, null=True)
    middle_name = models.CharField(max_length=60, null=True)
    email = models.CharField(max_length=60, null=True)
    phone = models.CharField(max_length=60, null=True)
    city = models.CharField(max_length=60, null=True)
    country = models.CharField(max_length=60, null=True)
    address = models.CharField(max_length=60, null=True)
    created_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.user.username



