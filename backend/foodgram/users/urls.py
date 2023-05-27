from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserMeViewSet, SetPasswordViewSet,
                    UsersViewSet)

app_name = 'users'

router = DefaultRouter()

router.register(
    'me',
    UserMeViewSet,
    basename='user_me'
)
router.register(
    'set_password',
    SetPasswordViewSet,
    basename='set_password'
)

router.register(
    '',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('users/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
