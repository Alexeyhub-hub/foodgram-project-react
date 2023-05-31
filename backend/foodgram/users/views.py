from api.pagination import CustomPagination
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Follow, User
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          FollowSerializer, SetPasswordSerializer)


class UserMeViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class SetPasswordViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'success': 'Password successfully changed'},
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        new_password = serializer.validated_data.get('new_password')
        self.request.user.set_password(new_password)
        self.request.user.save()


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return self.serializer_class
        return CustomUserCreateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        serializer_class=CustomUserSerializer
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(
            User,
            id=self.kwargs.get('pk')
        )
        if request.method == 'POST':
            serializer = FollowSerializer(
                author,
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        subscription = get_object_or_404(
            Follow,
            user=user,
            author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(follower__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
