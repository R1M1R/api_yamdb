from rest_framework import routers
from users.views import APIRegistrUser, APIGetToken
from django.urls import include, path
from api.views import (
    ReviewViewSet,
    CommentsViewSet
)

router = routers.DefaultRouter()
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
    path('v1/', include(router.urls)
]
