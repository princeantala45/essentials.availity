from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Device, SongSuggestion, FavoriteSong


def get_client_ip(request):

    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded:
        return forwarded.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


@api_view(["POST"])
def login_view(request):

    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    device_id = request.data.get("device_id", "")
    device_name = request.data.get("device_name", "")
    browser = request.data.get("browser", "")
    operating_system = request.data.get("operating_system", "")

    if not username or not password:
        return Response(
            {"status": "error", "message": "Username and password are required."},
            status=400
        )

    if not device_id:
        return Response(
            {"status": "error", "message": "Device ID is required."},
            status=400
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"status": "error", "message": "Invalid username or password."},
            status=401
        )

    device = Device.objects.filter(user=user, device_id=device_id).first()

    if device is None:
        device = Device.objects.create(
            user=user,
            device_id=device_id,
            device_name=device_name,
            browser=browser,
            operating_system=operating_system,
            ip_address=get_client_ip(request),
            status="pending"
        )

        return Response({
            "status": "pending",
            "message": "Please approve your device from the admin panel."
        })

    device.device_name = device_name
    device.browser = browser
    device.operating_system = operating_system
    device.ip_address = get_client_ip(request)
    device.last_seen = timezone.now()
    device.save()

    if device.status == "approved":
        return Response({"status": "approved", "message": "Login successful."})

    if device.status == "rejected":
        return Response({"status": "rejected", "message": "Your device has been rejected."})

    return Response({
        "status": "pending",
        "message": "Please approve your device from the admin panel."
    })


@api_view(["POST"])
def signup_view(request):

    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    confirm_password = request.data.get("confirm_password", "")
    email = request.data.get("email", "").strip()

    if not username or not password:
        return Response(
            {"status": "error", "message": "Username and password are required."},
            status=400
        )

    if password != confirm_password:
        return Response(
            {"status": "error", "message": "Passwords do not match."},
            status=400
        )

    if len(password) < 6:
        return Response(
            {"status": "error", "message": "Password must be at least 6 characters."},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"status": "error", "message": "Username already exists."},
            status=400
        )

    if email and User.objects.filter(email=email).exists():
        return Response(
            {"status": "error", "message": "Email already exists."},
            status=400
        )

    user = User.objects.create_user(username=username, email=email, password=password)

    return Response(
        {
            "status": "success",
            "message": "Account created successfully.",
            "username": user.username
        },
        status=201
    )


@api_view(["POST"])
def check_device(request):

    username = request.data.get("username", "").strip()
    device_id = request.data.get("device_id", "")

    if not username or not device_id:
        return Response(
            {"status": "denied", "message": "Invalid access."},
            status=400
        )

    device = Device.objects.filter(user__username=username, device_id=device_id).first()

    if device is None:
        return Response(
            {"status": "denied", "message": "Device not found."},
            status=403
        )

    device.last_seen = timezone.now()
    device.save(update_fields=["last_seen"])

    if device.status == "approved":
        return Response({"status": "approved", "message": "Access granted."}, status=200)

    if device.status == "rejected":
        return Response({"status": "rejected", "message": "Your device has been rejected."}, status=200)

    return Response({"status": "pending", "message": "Please approve your device."}, status=200)


def uptime_check(request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "All Music Backend",
            "message": "Backend is running"
        },
        status=200
    )

@api_view(["GET", "POST"])
def song_suggestion(request):

    if request.method == "GET":

        username = request.query_params.get("username", "").strip()

        if not username:
            return Response(
                {"status": "error", "message": "Username is required."},
                status=400
            )

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response(
                {"status": "error", "message": "User not found."},
                status=404
            )

        suggestions = SongSuggestion.objects.filter(user=user).order_by("-created_at")

        data = [
            {
                "song_name": s.song_name,
                "artist": s.artist,
                "category": s.category,
                "note": s.note,
                "status": s.status,
                "created_at": s.created_at,
            }
            for s in suggestions
        ]

        return Response(
            {"status": "success", "suggestions": data},
            status=200
        )

    # request.method == "POST"

    username = request.data.get("username", "").strip()
    song_name = request.data.get("song_name", "").strip()
    artist = request.data.get("artist", "").strip()
    category = request.data.get("category", "").strip()
    note = request.data.get("note", "").strip()

    if not username:
        return Response(
            {"status": "error", "message": "User not found."},
            status=400
        )

    if not song_name:
        return Response(
            {"status": "error", "message": "Please enter a song name."},
            status=400
        )

    user = User.objects.filter(username=username).first()

    if user is None:
        return Response(
            {"status": "error", "message": "User not found."},
            status=404
        )

    SongSuggestion.objects.create(
        user=user,
        song_name=song_name,
        artist=artist,
        category=category,
        note=note
    )

    return Response(
        {"status": "success", "message": "Song suggestion submitted successfully."},
        status=201
    )

@api_view(["GET"])
def suggestions_list(request):

    username = request.query_params.get("username", "").strip()

    if not username:
        return Response(
            {"status": "error", "message": "Username is required."},
            status=400
        )

    user = User.objects.filter(username=username).first()

    if user is None:
        return Response(
            {"status": "error", "message": "User not found."},
            status=404
        )

    suggestions = SongSuggestion.objects.filter(user=user).order_by("-created_at")

    data = [
        {
            "song_name": s.song_name,
            "artist": s.artist,
            "category": s.category,
            "note": s.note,
            "status": s.status,
            "created_at": s.created_at,
        }
        for s in suggestions
    ]

    return Response(
        {"status": "success", "suggestions": data},
        status=200
    )
    
    
@api_view(["GET"])
def favorites_list(request):

    username = request.query_params.get("username", "").strip()

    if not username:
        return Response(
            {
                "status": "error",
                "message": "Username is required."
            },
            status=400
        )

    user = User.objects.filter(username=username).first()

    if user is None:
        return Response(
            {
                "status": "error",
                "message": "User not found."
            },
            status=404
        )

    favorites = FavoriteSong.objects.filter(
        user=user
    ).order_by("-created_at")

    data = [
        {
            "category": favorite.category,
            "song_id": favorite.song_id,
        }
        for favorite in favorites
    ]

    return Response(
        {
            "status": "success",
            "favorites": data
        },
        status=200
    )


@api_view(["POST"])
def favorite_toggle(request):

    username = request.data.get("username", "").strip()
    category = request.data.get("category", "").strip()
    song_id = request.data.get("song_id", "").strip()

    if not username:
        return Response(
            {
                "status": "error",
                "message": "Username is required."
            },
            status=400
        )

    if not category or not song_id:
        return Response(
            {
                "status": "error",
                "message": "Category and song_id are required."
            },
            status=400
        )

    user = User.objects.filter(username=username).first()

    if user is None:
        return Response(
            {
                "status": "error",
                "message": "User not found."
            },
            status=404
        )

    favorite = FavoriteSong.objects.filter(
        user=user,
        category=category,
        song_id=song_id
    ).first()

    if favorite:
        favorite.delete()

        return Response(
            {
                "status": "success",
                "favorite": False,
                "message": "Removed from favorites."
            },
            status=200
        )

    FavoriteSong.objects.create(
        user=user,
        category=category,
        song_id=song_id
    )

    return Response(
        {
            "status": "success",
            "favorite": True,
            "message": "Added to favorites."
        },
        status=201
    )