from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from django.db import models

class Batch(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = None
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    country_code = models.CharField(max_length=5, blank=True)
    dob = models.DateField(null=True, blank=True)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    current_city = models.CharField(max_length=255, blank=True)
    workplace = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    is_external = models.BooleanField(default=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
