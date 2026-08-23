from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils import timezone

from .models import *


class DeviceInline(admin.TabularInline):

    model = Device

    extra = 0

    fields = (
        "device_name",
        "browser",
        "operating_system",
        "ip_address",
        "status",
        "created_at",
        "approved_at",
        "last_seen",
    )

    readonly_fields = (
        "device_name",
        "browser",
        "operating_system",
        "ip_address",
        "created_at",
        "approved_at",
        "last_seen",
    )

    def get_queryset(self, request):
        # Filter the inline queryset to show only pending devices
        qs = super().get_queryset(request)
        return qs.filter(status="pending")
class FavoriteSongInline(admin.TabularInline):

    model = FavoriteSong

    extra = 0

    fields = (
        "category",
        "song_id",
        "created_at",
    )

    readonly_fields = (
        "category",
        "song_id",
        "created_at",
    )


class CustomUserAdmin(UserAdmin):

    inlines = [
        DeviceInline,
        FavoriteSongInline,
    ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.action(description="Approve selected devices")
def approve_devices(modeladmin, request, queryset):

    queryset.update(
        status="approved",
        approved_at=timezone.now()
    )


@admin.action(description="Reject selected devices")
def reject_devices(modeladmin, request, queryset):

    queryset.update(
        status="rejected"
    )


@admin.action(description="Revoke selected devices")
def revoke_devices(modeladmin, request, queryset):

    queryset.update(
        status="pending",
        approved_at=None
    )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "device_name",
        "browser",
        "operating_system",
        "ip_address",
        "status",
        "created_at",
        "approved_at",
        "last_seen",
    )

    list_filter = (
        "status",
        "browser",
        "operating_system",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "device_name",
        "device_id",
        "ip_address",
    )

    readonly_fields = (
        "device_id",
        "created_at",
        "approved_at",
        "last_seen",
    )

    actions = [
        approve_devices,
        reject_devices,
        revoke_devices,
    ]


@admin.register(SongSuggestion)
class SongSuggestionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "song_name",
        "artist",
        "category",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "created_at",
    )

    search_fields = (
        "song_name",
        "artist",
        "user__username",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25


@admin.register(FavoriteSong)
class FavoriteSongAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "category",
        "song_id",
        "created_at",
    )

    list_filter = (
        "category",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "category",
        "song_id",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25