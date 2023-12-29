# from rest_framework import serializers
# from shop.serializers import ShopSerializer
# from user.serializers import ExpertCategorySerializer
# from user.models import CustomUser
#
#
# class UserPublicExpertSerializer(serializers.ModelSerializer):
#     expert_category = ExpertCategorySerializer(read_only=True)
#     profile_photo = serializers.ImageField()
#     shop_set = ShopSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = CustomUser
#         fields = (
#             'id', 'phone', 'email', 'whatsapp_number', 'full_name', 'address', 'pin_code', 'state', 'city', 'is_vendor',
#             'rating', 'profile_photo', 'latitude', 'longitude',
#             'expert_category', 'years_of_experience', "shop_set")
#
#     def get_profile_photo(self, obj):
#         return obj.profile_photo.url
