import datetime
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from decimal import Decimal


class Package(models.Model):
    name = models.CharField(max_length=50)
    percent = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    recommendation_bonus_usd = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_som = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name


class Node(MPTTModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, null=True)
    package = models.ForeignKey(Package, null=True, on_delete=models.DO_NOTHING)
    is_right = models.BooleanField(default=0)
    status = models.IntegerField(default=0, null=True)  # 1-active, 0-free
    total_point = models.IntegerField(default=0)
    left_point = models.IntegerField(default=0)
    right_point = models.IntegerField(default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    step = models.IntegerField(default=0)
    cycle = models.IntegerField(default=0)
    expired_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    inviter = models.ForeignKey("Node", null=True, blank=True, related_name='invited_children', on_delete=models.DO_NOTHING)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    is_processed = models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = "Nodes"

    def __str__(self):
        return self.name + get_status(self.status)


def get_status(status):
    if status == 0:
        return "    (неактивный)"
    if status == 1:
        return "    (активный)"
    return ""


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


class BonusType(models.Model):
    code = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Bonus(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="bonus_node", null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    partner = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="bonus_partner", null=True)
    type = models.CharField(max_length=60, null=True, blank=True)
    currency = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.value


class BonusSettings(models.Model):
    bonus_type = models.ForeignKey(BonusType, on_delete=models.CASCADE)
    bonus_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    level = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    right = models.IntegerField(default=0)
    diff = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.bonus_type.name


class PropertyValueSettings(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.name


