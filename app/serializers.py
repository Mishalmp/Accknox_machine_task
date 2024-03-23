

from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from .models import UserModel,FriendsModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model= UserModel
        fields = ['id',"email","password","username"]
        extra_kwargs={
            'password':{'write_only':True},
        }


    def validate_email(self, value):
        """
        validating email with case insensitive

        """
        if UserModel.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("this email already in use")
        return value
    

        
class MyTokenobtainpairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token["email"] = user.email
        token["username"] = user.username

        return token


class FriendsSerializer(serializers.ModelSerializer):
    to_user = UserModelSerializer(read_only=True) 
    from_user = UserModelSerializer(read_only=True)
    class Meta:
        model = FriendsModel
        fields = '__all__'
        read_only_fields = ('from_user', 'created_at', 'updated_at')
    

    def update(self, instance, validated_data):
            user = self.context["request"].user
            if user == instance.to_user:
                instance.status = validated_data.get('status', instance.status)
                instance.save()
                return instance
            else:
                raise serializers.ValidationError("You are not allowed to change the status!!!")
            




        
        