from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from api.models import StyleConfig

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "first_name", "last_name")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords didn’t match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user



class StyleConfigSerializer(serializers.ModelSerializer):
    def validate_class_names(self, value):
        if not value.strip():
            raise serializers.ValidationError("class_names cannot be empty.")
        return value
            
    class Meta:
        model = StyleConfig
        fields = ['id', 'platform', 'component_type', 'component_name', 'class_names', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']