from user.models import *
from django.core.validators import FileExtensionValidator


class Shop(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    file_extension_validator = FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])
    is_verified = models.BooleanField(default=False, null=False, blank=False)
    name = models.CharField(null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    whatsapp_number = models.CharField(blank=False, null=False, max_length=15, validators=[phone_regex])
    address = models.CharField(blank=False, null=False, max_length=150)
    pin_code = models.IntegerField(blank=False, null=False, max_length=15)
    expert_category = models.ForeignKey(ExpertCategory, null=True, blank=True, on_delete=models.DO_NOTHING)
    expert_subcategory = models.ForeignKey(ExpertSubcategory, null=True, blank=True, on_delete=models.DO_NOTHING)
    shop_cert = models.FileField(upload_to='uploads/shop_cert/', validators=[file_extension_validator], null=True,
                                 blank=True)

    REQUIRED_FIELDS = ['name', 'whatsapp_number', 'address', 'pin_code', 'expert_category',
                       'expert_subcategory', 'shop_cert']

    def __str__(self):
        return self.name
