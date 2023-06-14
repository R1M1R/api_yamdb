from django.urls import include, path
from user.views import APIRegistrUser, APIGetToken

auth_patterns = [
    path('signup/', APIRegistrUser.as_view(), name='register_user'),
    path('token/', APIGetToken.as_view(), name='get_token'),
]


urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
]
