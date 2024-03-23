
from .serializers import UserModelSerializer,MyTokenobtainpairSerializer,FriendsSerializer
from .models import UserModel,FriendsModel
# from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.throttling import UserRateThrottle
from .throttle import FriendRequestThrottle
# Create your views here.


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        #permissions allowed to any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are allowed to the owner or admin users
        return obj == request.user or request.user.is_superuser


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UsersView(ModelViewSet):
    serializer_class=UserModelSerializer
    queryset = UserModel.objects.all().exclude(is_superuser=True).order_by("-id")
    filter_backends = [SearchFilter]
    search_fields = ['email','username']

    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny] 
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdminOrReadOnly]  
        else:
            permission_classes = [IsAuthenticated]  

        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        hashed_password = make_password(password)
        serializer.save(password=hashed_password)


class MytokenobtainpairView(TokenObtainPairView):
    serializer_class=MyTokenobtainpairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self,request):

        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response({"message":"Logout Successfull"},status=status.HTTP_205_RESET_CONTENT)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class FriendsView(ModelViewSet):
    permission_classes = [IsAuthenticated] 
    throttle_classes = [FriendRequestThrottle,UserRateThrottle]
    serializer_class = FriendsSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = FriendsModel.objects.filter(from_user=user) | FriendsModel.objects.filter(to_user=user)

        sort = self.request.query_params.get('sort')

        if sort:
            if sort == "friends":
                queryset = FriendsModel.objects.filter(status="accepted",from_user=user) | FriendsModel.objects.filter(status="accepted",to_user=user)
            elif sort == "accepted":
                queryset = FriendsModel.objects.filter(status="accepted",from_user=user) 
            elif sort == 'pending':
                queryset = FriendsModel.objects.filter(from_user=user,status="pending")
            elif sort == 'rejected':
                queryset = FriendsModel.objects.filter(from_user=user,status="rejected")
            elif sort == 'requests':
                queryset = FriendsModel.objects.filter(to_user=user,status="pending")

        return queryset.order_by("-updated_at")
    


    def create(self, request, *args, **kwargs):
        to_user_data = request.data.pop('to_user')
        user = request.user
        to_user_instance = UserModel.objects.get(id=to_user_data['id'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(to_user=to_user_instance, from_user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    












