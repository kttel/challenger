import os

from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


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
    return os.path.join(f'images/{instance.TYPE}',
                        generate_uuid4_filename(filename))


class Challenge(models.Model):
    """
    Model that represents challenge entity.
    """
    TYPE = 'challenges'
    DEFAULT_IMAGE = 'default.jpg'
    title = models.CharField(max_length=255,
                             help_text="Enter your challenge title")
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.SET_NULL, null=True)
    short_intro = models.CharField(max_length=500,
                                   help_text="Provide short intro for your \
                                    challenge")
    description = models.TextField(help_text="Feel free to describe all \
                                   things related to challenge")
    image = models.ImageField(upload_to=get_file_path,
                              default=DEFAULT_IMAGE, blank=True)
    cover = models.ImageField(upload_to=get_file_path,
                              default=DEFAULT_IMAGE, blank=True)
    days = models.IntegerField()
    is_active = models.BooleanField(default=False)
    is_moderated = models.BooleanField(default=False)
    participants = models.ManyToManyField(get_user_model(),
                                          related_name='participants')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def toggle_active(self):
        self.is_active = not self.is_active

    def moderate(self):
        self.is_moderated = True

    def delete_image(self):
        """Sets image to default one."""
        self.image = self.DEFAULT_IMAGE

    def delete_cover(self):
        """Sets cover to default one."""
        self.cover = self.DEFAULT_IMAGE

    def __str__(self):
        return self.title


class Achievement(models.Model):
    """
    Model that represents an achievement entity.
    """
    TYPE = 'achievements'
    DEFAULT_IMAGE = 'default.jpg'

    class StyleChoices(models.TextChoices):
        BRONZE = 'B', _('Bronze')
        SILVER = 'S', _('Silver')
        GOLD = 'G', _('Gold')

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user = user = models.ForeignKey(get_user_model(),
                                    on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=175,
                             help_text="Enter challenge achievement name")
    description = models.TextField(help_text="Describe all possible ways \
                                   to get this achievement")
    style = models.CharField(max_length=10, help_text="Style of achievement",
                             choices=StyleChoices.choices,
                             default=StyleChoices.BRONZE, blank=True)
    icon = models.ImageField(upload_to=get_file_path,
                              default='default.jpg', blank=True)
    is_available = models.BooleanField(default=False)
    is_moderated = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def toggle_availability(self):
        self.is_available = not self.is_available

    def moderate(self):
        self.is_moderated = True

    def __str__(self):
        return self.title
