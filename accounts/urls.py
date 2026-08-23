from django.urls import path

from .views import (
    login_view,
    signup_view,
    uptime_check,
    check_device,
    song_suggestion,
    favorites_list,
    favorite_toggle,
)


   
   
urlpatterns = [

    path(
        "login/",
        login_view,
        name="login"
    ),

    path(
        "signup/",
        signup_view,
        name="signup"
    ),

    path(
        "check-device/",
        check_device,
        name="check_device"
    ),

    path(
        "uptime/",
        uptime_check,
        name="uptime_check"
    ),

    path(
        "suggestions/",
        song_suggestion,
        name="song_suggestion"
    ),

    path(
        "favorites/",
        favorites_list,
        name="favorites_list"
    ),

    path(
        "favorites/toggle/",
        favorite_toggle,
        name="favorite_toggle"
    ),
]