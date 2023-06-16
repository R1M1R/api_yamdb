from .models import User
from rest_framework import serializers
from api_yamdb.settings import NOT_ALLOWED_USERNAME

USERNAME_CHECK = r'^[\w.@+-]+$'


class RegistrUserSerializer(serializers.Serializer):

    username = serializers.RegexField(
        regex=USERNAME_CHECK,
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.confirmation_code = validated_data.get(
            "confirmation_code",
            instance.confirmation_code
        )
        instance.save()
        return instance

    def validate(self, data):
        if data['username'] == NOT_ALLOWED_USERNAME:
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено.'
            )
        return data

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.Serializer):

    username = serializers.RegexField(
        regex=USERNAME_CHECK,
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=8,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
