from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,permissions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import FriendRequest
from .serializers import UserSerializer,LoginSerializer,RequestSerializer
from rest_framework import exceptions
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
import itertools
from .throttling import FriendRequestThrottle
from rest_framework.authentication import TokenAuthentication

# Create your views here.
User = get_user_model()

# Api is for signup
# it type of post method
# which accepts user as bosy with first_name,last_name,username,email and password
class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    
# Api is for login
# it type of post method
# which accepts user as bosy with username and password
# Raise an authentication exception if the user does not exist
# return the created token for the user which will be used for furthur api 

class loginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            try:
                userdata= User.objects.get(username=user["username"],password=user["password"])
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such user')
            token, created =Token.objects.get_or_create(user=userdata)
            return Response({"message":userdata.first_name+" is logged in.",
                  'token': token.key,
            })  
        return Response(serializer.error) 

class SetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
 
# Api is for 
# it type of get method
# which accepts  as query_params search_text

class SearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = SetPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get_queryset(self):
        query = self.request.query_params.get('search_text')
        return User.objects.filter(

            Q(first_name__icontains=query)| Q(email__icontains=query)
                                           
        )


# Api is For send friend request 
# it type of post method
# which accept query_params from_user & to_user

class SendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self,request):
        from_user = request.query_params.get('from_user')
        touserData=self.request.query_params.get('to_user')
        to_user = User.objects.get(username=touserData)
        from_user_data = User.objects.get(username=from_user)
        print(from_user_data)
        now = timezone.now()
        one_minutes_ago = now - timedelta(minutes=1)
        print("one_minutes_ago ", one_minutes_ago)
        requests_count = FriendRequest.objects.filter(
                from_user = from_user_data,created_at__gte = one_minutes_ago)
        if requests_count.count() >=3:
            return Response({'error': 'You cannot send more than 3 friend requests within a minute.'})
        if FriendRequest.objects.filter(from_user=from_user_data,to_user=to_user).exists():
            return Response({'detail':'Friend request already sent'})
        friend_request = FriendRequest(from_user = from_user_data,to_user= to_user)
        friend_request.save()
        return Response(RequestSerializer(friend_request).data)
    

# Api for respond friend request
# it type of post method
# which accept query_params from ,to & action 

class RespondRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self,request):
     
        request_name = request.query_params.get('from')
        touserData=self.request.query_params.get('to')
        fromUser=User.objects.get(username=request_name)
        toUser=User.objects.get(username=touserData)
        
        # if friend_request.to_user != request.user:
        #      return Response({'detail': 'Not your friend request'})
        action = request.query_params.get('action')
        if not action :
            raise exceptions.ValidationError('No action provided')
        friend_request = FriendRequest.objects.get(from_user=fromUser,to_user=toUser)

        if friend_request.status != 'sent':
           raise exceptions.ValidationError('No sent request available')
        if action == 'accept':
            friend_request.status ='accepted'
        elif action == 'reject':
            friend_request.status = 'rejected'
        else:
             raise exceptions.ValidationError('No action provided')
        friend_request.save()
        return Response(RequestSerializer(friend_request).data)
         
        
       
        
 # Api for friendlist
 # it type of get method
 # Which accepted query_params username 
 # which returns only accepted user   

class ListFriendsView(generics.ListAPIView):

   permission_classes = [permissions.IsAuthenticated]
   authentication_classes=[TokenAuthentication]
   serializer_class = UserSerializer
   data_class= RequestSerializer
   def get(self,request):
       from_user = request.query_params.get("username")
       userData=User.objects.get(username=from_user)
       friends= FriendRequest.objects.filter(Q(from_user=userData,status="accepted" )|
                                     Q(to_user=userData,status="accepted"))
       attribute_list = [obj.from_user for obj in friends]
       attribute_list.extend([obj.to_user for obj in friends])
       filtered_lists = list(itertools.filterfalse
                             (lambda x: x.username == from_user, attribute_list)
                             )

       serializer = UserSerializer(filtered_lists, many=True)
       return Response(serializer.data)
       
# Api for pendinglist
# it type of get method
# Which accepted query_params username  
    
class ListPendingFriendView(APIView):
     permission_classes = [permissions.IsAuthenticated]
     authentication_classes=[TokenAuthentication]
     def get(self,request):
         user = request.query_params.get("username")
         userData=User.objects.get(username=user)
         pending_requests = FriendRequest.objects.filter(to_user=userData,status="sent")
         attribute_list = [obj.from_user for obj in pending_requests]
         serializer = UserSerializer(attribute_list, many=True)
         return Response(serializer.data)



















    
    

           


   
      
      
      
 



#def get_object(self):
  #      return self.request.user
