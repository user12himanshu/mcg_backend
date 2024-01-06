from rest_framework import serializers
from user.serializers import ExpertCategorySerializer, UserSerializer
from shop.serializers import ShopSerializer
from .models import *


class AutoFindSerializer(serializers.ModelSerializer):
    expert_category = ExpertCategorySerializer(read_only=True)
    profile_photo = serializers.ImageField()
    shop_set = ShopSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'phone', 'email', 'whatsapp_number', 'full_name', 'address', 'pin_code', 'state', 'city', 'is_vendor',
            'rating', 'profile_photo', 'latitude', 'longitude',
            'expert_category', 'years_of_experience', "shop_set")

    def get_profile_photo(self, obj):
        return obj.profile_photo.url


# class NofiticationSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = Notification
#         fields = '__all__'

class ConsultUsSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(read_only=True)
    end_time = serializers.TimeField(read_only=True)
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Slot
        fields = "__all__"


# class ConsultUsAvailableSlotsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Slot
#         fields = ("date")


class ChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charges
        fields = "__all__"


class InitPaymentSerializer(serializers.Serializer):
    product = serializers.CharField(required=True)
    owner = serializers.IntegerField(required=True)
    phone = serializers.CharField(required=True)
