
from django.urls import path,include
from .views import MytokenobtainpairView,LogoutView,FriendsView,UsersView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('friends',FriendsView,basename='friends')
router.register('users',UsersView,basename='users')

urlpatterns = [
    path('',include(router.urls)),
    path('token/', MytokenobtainpairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
