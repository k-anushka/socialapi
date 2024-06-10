from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()



# class User(User):
#      pass
# # Create your models here.



class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_request', on_delete= models.CASCADE)
    to_user = models.ForeignKey(User, related_name='recevied_request',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=[('sent','Sent'),('accepted','Accepted'),('rejected','Rejected')],default='sent')
    

    class Meta:
        unique_together = ('from_user','to_user')

    










