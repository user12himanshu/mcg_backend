from rest_framework import serializers
from .models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user:
            raise serializers.ValidationError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise serializers.ValidationError("You are not allowed to perform this action.")
        query_set = Shop.objects.filter(owner=user, name=attrs.get('name'), pin_code=attrs.get('pin_code'))

        if query_set.exists():
            raise serializers.ValidationError("Shop with similar name exists")
        return attrs
