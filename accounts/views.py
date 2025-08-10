from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UsersSerializer

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    """
    Создание нового пользователя (регистрация)
    Доступ: всем (публичный endpoint)
    """

    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserListAPIView(generics.ListAPIView):
    """
    Получить список всех пользователей
    Доступ: только админам
    """

    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Получить детальную информацию о пользователе по ID
    (только для админов)
    put:
    Обновление всех полей пользователя по ID
    (только для админов)
    patch:
    Обновление отдельных полей пользователя по ID
    (только для админов)
    delete:
    Полное удаление информации о пользователе по ID
    (только для админов)
    """

    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        """Запретить удаление суперпользователя обычными админами"""
        instance = self.get_object()
        if instance.is_superuser and not request.user.is_superuser:
            return Response(
                {"detail": "Только суперпользователь может удалять других суперпользователей"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class UserMeAPIView(generics.RetrieveUpdateAPIView):
    """
    Получить/обновить информацию о текущем пользователе
    Доступ: авторизованным пользователям
    Обновление: только безопасные поля
    """

    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Возвращаем текущего пользователя"""
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Запретить изменение важных полей через этот endpoint"""
        # Удаление чувствительных полей из запроса
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Запрет на изменение email, is_staff, is_superuser через /me/
        data = request.data.copy()
        sensitive_fields = ['email', 'is_staff', 'is_superuser', 'is_active']
        for field in sensitive_fields:
            if field in data:
                data.pop(field)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
