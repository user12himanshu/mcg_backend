from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from mcg.utility import phone_regex


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, confirm_password, phone, **extra_fields):
        if not email:
            raise ValueError("The email is not given.")

        if not phone:
            raise ValueError("The phone is not given.")

        if not password == confirm_password:
            raise ValueError("Passwords don't match")

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff = True")

        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(email, password, **extra_fields)


class ExpertCategory(models.Model):
    category = models.CharField(unique=True, blank=False, null=False)


class ExpertSubcategory(models.Model):
    sub_category = models.CharField(unique=True, blank=False, null=False)
    category = models.ForeignKey(ExpertCategory, on_delete=models.CASCADE)


class CustomUser(AbstractBaseUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+123456789'. Up to 10 digits allowed."
    )
    file_extension_validator = FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])
    #TODO: Add logic to add country code in phone for both frontend and backend.
    phone = models.CharField(unique=True, blank=False, null=False, max_length=15, validators=[phone_regex])
    whatsapp_number = models.CharField(blank=False, null=False, max_length=15, validators=[phone_regex])
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(blank=False, null=False, max_length=100)
    confirm_password = models.CharField(blank=False, null=False, max_length=100)
    full_name = models.CharField(blank=False, null=False, max_length=100)
    address = models.CharField(blank=False, null=False, max_length=150)
    pin_code = models.IntegerField(blank=False, null=False, max_length=15)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    otp = models.IntegerField(max_length=6, blank=True, null=True)
    is_otp_verified = models.BooleanField(default=False)
    expert_category = models.ForeignKey(ExpertCategory, null=True, blank=True, on_delete=models.DO_NOTHING)
    expert_subcategory = models.ForeignKey(ExpertSubcategory, null=True, blank=True, on_delete=models.DO_NOTHING)
    years_of_experience = models.IntegerField(blank=True, null=True)
    # TODO: Add file size validation to file fields
    aadhar_card = models.FileField(upload_to='uploads/aadhar_card/', validators=[file_extension_validator], null=True,
                                   blank=True)
    pan_card = models.FileField(upload_to='uploads/pan_card/', validators=[file_extension_validator], null=True,
                                blank=True)
    driving_card = models.FileField(upload_to='uploads/driving_card/', validators=[file_extension_validator], null=True,
                                    blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['password', 'confirm_password', 'full_name', 'address', 'pin_code', 'whatsapp_number', 'email']

    objects = UserManager()

    def __str__(self):
        return self.phone

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
