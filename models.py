from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

# Custom User Manager to handle 'status' field
class RecruiterManager(BaseUserManager):
    def create_user(self, username, email, password=None, status="AWAITING_APPROVAL", **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, status=status, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

# Custom Recruiter Model
class Recruiter(AbstractUser):
    STATUS_CHOICES = [
        ('AWAITING_APPROVAL', 'Awaiting Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AWAITING_APPROVAL')

    groups = models.ManyToManyField(Group, related_name="recruiter_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="recruiter_permissions", blank=True)

    objects = RecruiterManager()  # Assign custom manager

    def __str__(self):
        return self.username
