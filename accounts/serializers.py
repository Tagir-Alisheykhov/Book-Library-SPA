from rest_framework import serializers

from accounts.models import User


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'avatar', 'is_active', 'is_staff',
            'is_superuser', 'date_joined', 'password'
        ]
        read_only_fields = ['id', 'is_active', 'is_staff', 'is_superuser', 'date_joined']

    def create(self, validated_data):
        """Шифрование пароля при создании"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def update(self, instance, validated_data):
        """Шифрование пароля при обновлении"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для /me/ endpoint - ограниченный доступ"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'avatar'
        ]
        read_only_fields = ['id', 'email']
