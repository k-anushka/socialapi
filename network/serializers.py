from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import FriendRequest

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password',]
        extra_kwargs = {'password': {'write_only': True}}

   
        

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email']           
            )
        user.first_name= validated_data['first_name']
        user.last_name= validated_data['last_name']
        user.password= validated_data['password']
        User.save(user)
        return user
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id','from_user','to_user','status','created_at']
