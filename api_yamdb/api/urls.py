from rest_framework import routers
from users.views import APIRegistrUser, APIGetToken
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, GenreViewSet,
                       TitleViewSet, UsersViewSet,
                       ReviewViewSet, CommentsViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', APIRegistrUser.as_view(), name='register_user'),
    path('token/', APIGetToken.as_view(), name='get_token'),
]


urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router.urls)),
]
