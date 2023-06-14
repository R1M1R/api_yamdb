from user.serializers import RegistrUserSerializer, GetTokenSerializer
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User


class APIRegistrUser(APIView):

    def post(self, request):
        serializer = RegistrUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            username=serializer.validated_data.get('username')
        ).first()
        if user:
            serializer = RegistrUserSerializer(
                data=request.data,
                instance=user
            )
            serializer.is_valid(raise_exception=True)
        confirmation_code = 'TEST' ##Дописать генерацию 
        serializer.save(confirmation_code=confirmation_code)
        send_mail(
            subject='Регистрация.',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_EMAIL,
            recipient_list=[serializer.validated_data.get('email')]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            username=serializer.validated_data.get('username')
        ).first()
        if not user:
            return Response('Пользователь не найден',
                            status=status.HTTP_404_NOT_FOUND)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if user.confirmation_code != confirmation_code:
            return Response(
                'Неверный проверочный код',
                status=status.HTTP_400_BAD_REQUEST
            )
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )
