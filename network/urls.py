
from django.urls import path, include
from .views import SignupView,loginView, SearchView,SendRequestView, RespondRequestView,ListFriendsView,ListPendingFriendView
                     
urlpatterns = [
    path('signup/',SignupView.as_view(), name= 'signup'),
    path ('login/',loginView.as_view(), name='login'),
    path('search/',SearchView.as_view(), name='search'),
    path('send/',SendRequestView.as_view(), name = 'send'),
    path('respond/', RespondRequestView.as_view(), name='respond'),
    path('list_friends/', ListFriendsView.as_view(), name='list_friends'),
    path('list_pending_requests/',ListPendingFriendView.as_view(), name='list_pending_requests')
]


