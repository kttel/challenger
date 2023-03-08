import os

from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

from challenges.models import Achievement


def generate_uuid4_filename(filename):
    """
    Generates a random filename, keeping file extension.
    """
    discard, ext = os.path.splitext(filename)
    basename = str(uuid4())
    return basename + ext


def get_file_path(instance, filename):
    """
    Returns generated file path for image.
    """
    return os.path.join(f'images/users', generate_uuid4_filename(filename))


class Profile(models.Model):
    """
    Model that represents user profile to extend default user model.
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(help_text="Tell others about yourself!",
                           null=True, blank=True)
    avatar = models.ImageField(upload_to=get_file_path, default='d_user.png',
                               blank=True)
    social_link = models.CharField(max_length=2048, help_text="Add link for \
                                   your profile on any social media",
                                   null=True, blank=True)
    achievements = models.ManyToManyField(Achievement)
