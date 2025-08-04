from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# Create your models here.
class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    bio=models.TextField(blank=True,null=True)
    is_verified=models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

User=get_user_model()

class StyleConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='styles')
    platform = models.CharField(max_length=50, choices=[('tailwind', 'Tailwind'), ('bootstrap', 'Bootstrap')])
    component_type = models.CharField(max_length=100, choices=[
        ('layout', 'Layout'),
        ('navigation', 'Navigation'),
        ('forms', 'Forms'),
        ('buttons', 'Buttons'),
        ('feedback', 'Feedback'),
        ('data_display', 'Data Display'),
        ('special', 'Special'),
    ])
    component_name = models.CharField(max_length=100)
    class_names = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'platform', 'component_type', 'component_name')

    def __str__(self):
        return f"{self.user.username} - {self.platform} - {self.component_name}"