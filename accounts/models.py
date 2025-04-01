'''
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USER_TYPES = (
        ('recruiter', 'Recruiter'),
        ('job_seeker', 'Job Seeker'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='job_seeker')

    def __str__(self):
        return f"{self.username} - {self.user_type}"
'''
import uuid 
from datetime import datetime, timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .manager import CustomUserManager


class TokenType(models.TextChoices):
    PASSWORD_RESET = ("PASSWORD_RESET", "PASSWORD_RESET")


class User(AbstractBaseUser, PermissionsMixin):  # Remove models.Model
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

'''
class User(models.Model, AbstractBaseUser, PermissionsMixin):  # Changed BaseModel to models.Model
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
'''

class PendingUser(models.Model):  # Changed BaseModel to models.Model # I created this table manually in MySQL workbench using query.
    email = models.EmailField()
    password = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60  # 20 minutes validity
        now = datetime.now(timezone.utc)
        timediff = (now - self.created_at).total_seconds()
        return timediff <= lifespan_in_seconds


class Token(models.Model):  # Changed BaseModel to models.Model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=100, choices=TokenType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}  {self.token}"

    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60  # 20 minutes validity
        now = datetime.now(timezone.utc)
        timediff = (now - self.created_at).total_seconds()
        return timediff <= lifespan_in_seconds

    def reset_user_password(self, raw_password: str):
        self.user.set_password(raw_password)
        self.user.save()

'''
class TokenType(models.TextChoices):
    PASSWORD_RESET = ("PASSWORD_RESET", "PASSWORD_RESET")


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()


class PendingUser(BaseModel):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60  # 20 minutes
        now = datetime.now(timezone.utc)
        return (now - self.created_at).total_seconds() <= lifespan_in_seconds


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=100, choices=TokenType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}  {self.token}"

    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60  # 20 minutes
        now = datetime.now(timezone.utc)
        return (now - self.created_at).total_seconds() <= lifespan_in_seconds

    def reset_user_password(self, raw_password: str):
        self.user.set_password(raw_password)
        self.user.save()
'''
