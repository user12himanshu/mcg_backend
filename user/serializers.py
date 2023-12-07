from rest_framework import serializers
from .models import CustomUser, ExpertCategory
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'phone', 'email', 'whatsapp_number', 'full_name', 'address', 'pin_code', 'city', 'state','is_vendor')


class ExpertCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertCategory
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'phone', 'whatsapp_number', 'email', 'password', 'confirm_password', 'full_name', 'address', 'pin_code',
            'is_vendor', 'city', 'state')

    #
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        if attrs.get('is_vendor'):
            raise serializers.ValidationError('Something went wrong')
        if not (attrs.get('password') == attrs.get('confirm_password')):
            raise serializers.ValidationError('Passwords do not match')
        return attrs


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'phone', 'email', 'full_name', 'address', 'pin_code', 'whatsapp_number', 'city', 'state')

    def update(self, instance, validated_data):
        # print(validated_data)
        if validated_data.__contains__('password'):
            password = validated_data.pop('password')
            if password:
                instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance


class CreateVendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        if not attrs.get('is_vendor'):
            raise serializers.ValidationError('Something went wrong')
        if not attrs.get('expert_category'):
            raise serializers.ValidationError('Expert Category is required')
        if not attrs.get('expert_subcategory'):
            raise serializers.ValidationError('Expert SubCategory is required')
        if not attrs.get('years_of_experience'):
            raise serializers.ValidationError('Year of Experience is required')
        if not attrs.get('aadhar_card'):
            raise serializers.ValidationError('Aadhar card is required')
        if not attrs.get('pan_card'):
            raise serializers.ValidationError('Pan card is required')
        if not attrs.get('driving_card'):
            raise serializers.ValidationError('Driving card is required')

        if not (attrs.get('password') == attrs.get('confirm_password')):
            raise serializers.ValidationError('Passwords do not match')

        return attrs


class UpdateVendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'phone', 'email', 'full_name', 'address', 'pin_code', 'whatsapp_number', 'expert_category',
            'expert_subcategory', 'years_of_experience', 'city', 'state')

    def update(self, instance, validated_data):
        # print(validated_data)
        # self.context.get('request').user

        if validated_data.__contains__('password'):
            password = validated_data.pop('password')
            if password:
                instance.set_password(password)
        instance = super().update(instance, validated_data)
        return instance


class LoginSerializer(serializers.Serializer):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+123456789'. Up to 10 digits allowed."
    )
    phone = serializers.CharField(validators=[phone_regex])
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    is_vendor = serializers.BooleanField(default=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if not phone or not password:
            raise serializers.ValidationError('Please provide both email and password')
        if CustomUser.objects.filter(phone=phone).exists():
            if attrs.__contains__('is_vendor'):
                if attrs.get('is_vendor'):
                    if not CustomUser.objects.filter(phone=phone).first().is_vendor:
                        raise serializers.ValidationError('Please register as expert!')
            user = authenticate(request=self.context.get('request'), phone=phone, password=password)

            if not user:
                raise serializers.ValidationError('Wrong phone or password')

            attrs['user'] = user
        else:
            raise serializers.ValidationError('Account not found! Please register')

        return attrs