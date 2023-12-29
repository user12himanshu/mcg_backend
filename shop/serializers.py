from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer
# from mcg.serializers import UserPublicExpertSerializer
# from autofind.serializers import AutoFindSerializer


class ShopImagesSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField()

    class Meta:
        model = ShopImages
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    shop_images = ShopImagesSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Shop
        fields = ('owner', 'is_verified', 'name', 'email', 'whatsapp_number', 'address', 'pin_code',
                  'shop_cert', 'shop_images', 'id')

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user:
            raise serializers.ValidationError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise serializers.ValidationError("You are not allowed to perform this action.")
        # query_set = Shop.objects.filter(owner=user, name=attrs.get('name'), pin_code=attrs.get('pin_code'))
        #
        # if query_set.exists():
        #     raise serializers.ValidationError("Shop with similar name exists")
        return attrs


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    description = DescriptionSerializer(many=True, read_only=True)
    about = AboutSerializer(many=True, read_only=True)
    product_images = ProductImagesSerializer(many=True, read_only=True)
    owner = ShopSerializer(read_only=True)

    # discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = (
            'owner', 'description', 'name', 'price', 'discount', 'rating', 'id', 'about', 'product_images',
            'profile_photo', 'quanitity_in_stock', 'sales_price')

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user:
            raise serializers.ValidationError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise serializers.ValidationError("You are not allowed to perform this action.")
        # query_set = Shop.objects.filter(owner=attrs.get("owner"), name=attrs.get('name'))
        #
        # if query_set.exists():
        #     raise serializers.ValidationError("product with similar name exists")
        return attrs


class CartItemSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'products', 'owner', 'quantity', 'date_added', 'total_price', 'total_price_mrp')


class OrderItemSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('products', 'owner', 'quantity', 'date_added')
