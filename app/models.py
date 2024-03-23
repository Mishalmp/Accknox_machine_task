from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserModel(AbstractUser):

    email = models.EmailField(unique=True)


class FriendsModel(models.Model):

    STATUS=[
        ("pending","Pending"),
        ("accepted","Accepted"),
        ("rejected","Rejected")
    ]

    from_user = models.ForeignKey(UserModel,related_name="send_requests",on_delete = models.CASCADE)
    to_user = models.ForeignKey(UserModel,related_name = "received_requests",on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=STATUS,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = ['from_user',"to_user"]

    def __str__(self):
        return f"Friend request from {self.from_user.username} to {self.to_user.username} - {self.status}"

