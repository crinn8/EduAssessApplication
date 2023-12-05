from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField, Sum, BooleanField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for techno_q26_backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    email = EmailField(_('email address'), blank=False, unique=True)
    is_student = BooleanField(_('Is Student'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username'
    ]

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
