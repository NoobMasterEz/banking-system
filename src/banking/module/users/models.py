import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from banking.module.cores.models import Info
from banking.module.cores import defult


class User(AbstractUser):
    password = models.CharField(_("password"), max_length=128)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class Customer(Info):
    guid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    address = models.TextField()
    identity_number = models.CharField(max_length=13, unique=True)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name="customer")
    gender = models.CharField(choices=defult.SEX_CHOICES, max_length=6)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk': self.pk})

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.user.first_name, self.user.last_name)
        return full_name.strip()
