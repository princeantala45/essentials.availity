from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="devices"
    )

    device_id = models.CharField(
        max_length=255,
        unique=True
    )

    device_name = models.CharField(
        max_length=255,
        blank=True
    )

    browser = models.CharField(
        max_length=100,
        blank=True
    )

    operating_system = models.CharField(
        max_length=100,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    last_seen = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Device Approval"
        verbose_name_plural = "Device Approvals"

    def __str__(self):
        return f"{self.user.username} - {self.device_name}"
    
    
from django.contrib.auth.models import User
from django.db import models


class SongSuggestion(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("added", "Added"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="song_suggestions"
    )

    song_name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Song Suggestion"
        verbose_name_plural = "Song Suggestions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.song_name}"   
    
    
class FavoriteSong(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_songs"
    )
    category = models.CharField(max_length=255)
    song_id = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "category", "song_id")