from user.models import *
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator


class ShopImages(models.Model):
    image_extension_validator = FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])
    profile_photo = models.ImageField(upload_to='media/shop_photo/', validators=[image_extension_validator],
                                      null=True,
                                      blank=True)
    REQUIRED_FIELDS = ['profile_photo']


class ProductImages(models.Model):
    image_extension_validator = FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])
    profile_photo = models.ImageField(upload_to='media/product_photo/', validators=[image_extension_validator],
                                      null=True,
                                      blank=True)
    REQUIRED_FIELDS = ['profile_photo']


class Description(models.Model):
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    REQUIRED_FIELDS = ['label', 'description']


class About(models.Model):
    text = models.TextField(blank=False, null=False)
    REQUIRED_FIELDS = ['text']


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
    shop_images = models.ManyToManyField(ShopImages)

    REQUIRED_FIELDS = ['name', 'whatsapp_number', 'address', 'pin_code', 'shop_cert']

    def __str__(self):
        return self.name


class Products(models.Model):
    image_extension_validator = FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.ManyToManyField(Description)
    about = models.ManyToManyField(About)
    owner = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=False, null=False)
    price = models.DecimalField(max_digits=30, decimal_places=2)
    discount = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    quanitity_in_stock = models.IntegerField(default=0)
    rating = models.IntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(0)])
    product_images = models.ManyToManyField(ProductImages, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='media/product_photo/', validators=[image_extension_validator],
                                      null=True,
                                      blank=True)

    @property
    def sales_price(self):
        return "%.2f" % (float(self.price) - (float(self.price) * (float(self.discount) / 100)))

    REQUIRED_FIELDS = ['name', 'description', 'about', 'owner', 'price', 'rating', 'profile_photo']

    def __str__(self):
        return self.name


class CartItem(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(default=1)

    date_added = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['owner', 'quantity', 'date_added', 'products']

    @property
    def total_price(self):
        return "%.2f" % (float(self.products.sales_price) * float(self.quantity))

    @property
    def total_price_mrp(self):
        return "%.2f" % (float(self.products.price) * float(self.quantity))

    def __str__(self):
        return self.products.name + " " + self.owner.phone


class Order(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(default=1)

    date_added = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['owner', 'quantity', 'date_added', 'products']

# class SubscriptionCharges(models.Model):
#     monthly = models.DecimalField(decimal_places=2)
#     yearly = models.DecimalField(decimal_places=2)
#      = models.DecimalField(decimal_places=2)
