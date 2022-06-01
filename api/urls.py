from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import MyLoginView, PostViewSet, SignUpView

router = DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("login/", MyLoginView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
