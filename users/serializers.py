from rest_framework import serializers
from users.models import User, Borrower


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'personal_number', 'birth_date']
        required_fields = ['first_name', 'last_name', 'email', 'password', 'personal_number', 'birth_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['profile'] = User.UserProfile.BORROWER
        user = User.objects.create_user(**validated_data)
        Borrower.objects.create(user=user)
        return user


class BorrowerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Borrower
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {'photo': {'required': False}}
