from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from .choices import *
from django.conf import settings
User = settings.AUTH_USER_MODEL
import uuid

def validate_file_size(value):
    from django.core.exceptions import ValidationError
    filesize= value.size
    
    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, phone, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    phone = models.CharField(max_length=20, default=None, null=True, unique=True)
    username = models.CharField(max_length=30, unique=True)# Keep the username field
    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Custom fields
    uniqueid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    nick_name = models.CharField(max_length=100, null=True, blank=True)
    picture = models.ImageField(upload_to="profile_picture/", blank=True, null=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other')
    birth_day = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    mobile_otp = models.CharField(max_length=10, null=True, blank=True)
    email_otp = models.CharField(max_length=10, null=True, blank=True)
    pin = models.CharField(max_length=4, null=True, blank=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'phone'  # Set phone as the USERNAME_FIELD
    REQUIRED_FIELDS = ['username', 'email']  # Require username and email during user creation

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None): #This method checks whether the user has a specific permission (perm) on an object (obj). It returns True if the user has the permission, and False otherwise.
        # Adjust this method to check user permissions based on roles
        return self.is_superuser

    def has_module_perms(self, app_label): #This method checks whether the user has any permissions for a given application label (app_label). It returns True if the user has permissions for the app, and False otherwise.
        # Adjust this method to check user permissions based on roles
        return self.is_superuser

class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.country}"

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField()
    opening_hours = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=(('Success', 'Success'), ('Failed', 'Failed')))
    # Add additional fields as needed
