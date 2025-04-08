from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.http import HttpRequest
from accounts.models import PendingUser, Token, TokenType
from .decorators import redirect_authenticated_user
from .tasks import send_email

User = get_user_model()

def home(request):
    print("Home page view function running.")
    return render(request, "home.html")

@redirect_authenticated_user
def login(request: HttpRequest):
    """Handle user login."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()

        user = auth.authenticate(request, email=email, password=password)

        if user:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    return render(request, "accounts/login.html")

def logout(request: HttpRequest):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

@redirect_authenticated_user
def register(request: HttpRequest):
    """Register a new user with email verification."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect("register")

        verification_code = get_random_string(10)
        PendingUser.objects.update_or_create(
            email=email,
            defaults={
                "password": make_password(password),
                "verification_code": verification_code,
                "created_at": now(),
            },
            )

        send_email.delay(
            subject="Verify Your Account",
            email_to=[email],
            html_template="emails/email_verification_template.html",
            context={"code": verification_code},
        )

        messages.success(request, f"Verification code sent to {email}.")
        return render(request, "accounts/verify_account.html", {"email": email})

    return render(request, "accounts/register.html")


def verify_account(request: HttpRequest):
    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        email = request.POST.get("email", "").strip().lower()

        pending_user = PendingUser.objects.filter(
            verification_code=code, email=email
        ).first()

        if pending_user and pending_user.is_valid():
            user = User.objects.create(
                email=pending_user.email, password=pending_user.password
            )
            pending_user.delete()
            auth.login(request, user)
            messages.success(request, "Account verified! You are now logged in.")
            return redirect("home")

        messages.error(request, "Invalid or expired verification code.")
        return render(request, "accounts/verify_account.html", {"email": email}, status=400)

    return redirect("home")


def send_password_reset_link(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        user = User.objects.filter(email=email).first()

        if user:
            token, _ = Token.objects.update_or_create(
                user=user,
                token_type=TokenType.PASSWORD_RESET,
                defaults={
                    "token": get_random_string(20),
                    "created_at": now(),
                },
            )

            email_data = {"email": email, "token": token.token}
            send_email.delay(
                subject="Your Password Reset Link",
                email_to=[email],
                html_template="emails/password_reset_template.html",
                context=email_data,
            )

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect("reset_password_via_email")

        messages.error(request, "No account found with this email.")
        return redirect("reset_password_via_email")

    return render(request, "accounts/forgot_password.html")


def verify_password_reset_link(request: HttpRequest):
    email = request.GET.get("email", "").strip().lower()
    reset_token = request.GET.get("token", "").strip()

    token = Token.objects.filter(
        user__email=email, token=reset_token, token_type=TokenType.PASSWORD_RESET
    ).first()

    if not token or not token.is_valid():
        messages.error(request, "Invalid or expired reset link.")
        return redirect("reset_password_via_email")

    return render(
        request,
        "set_new_password_using_reset_token.html",
        {"email": email, "token": reset_token},
    )


def set_new_password_using_reset_link(request: HttpRequest):
    if request.method == "POST":
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()
        email = request.POST.get("email", "").strip().lower()
        reset_token = request.POST.get("token", "").strip()

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(
                request,
                "set_new_password_using_reset_token.html",
                {"email": email, "token": reset_token},
            )

        token = Token.objects.filter(
            token=reset_token, token_type=TokenType.PASSWORD_RESET, user__email=email
        ).first()

        if not token or not token.is_valid():
            messages.error(request, "Invalid or expired reset link.")
            return redirect("reset_password_via_email")

        token.reset_user_password(password1)
        token.delete()
        messages.success(request, "Your password has been successfully changed.")
        return redirect("login")

    return redirect("reset_password_via_email")
