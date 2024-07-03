from rest_framework import serializers
from users.models import User
from application_service.models import CandidateProfile, Application
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'password2')
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
       
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'name': self.user.name})
        return data


class CandidateProfileSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()

    class Meta:
        model = CandidateProfile
        fields = ('user','name', 'last_name', 'education', 'experience','photo', 'phone_number', 'address')
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('password2')
        user = User.objects.create_user(**user_data)
        candidate_profile = CandidateProfile.objects.create(user=user, **validated_data)
        return candidate_profile
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.education = validated_data.get('education', instance.education)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        user.email = user_data.get('email', user.email)
        user.name = user_data.get('name', user.name)
        user.set_password(user_data.get('password'))  # Update password if provided
        user.save()

        return instance
    

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['candidate']

        