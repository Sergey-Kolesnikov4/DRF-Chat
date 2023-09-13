from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name=models.CharField(max_length=120)
    members=models.ManyToManyField(User,related_name='members')
    def __str__(self):
        return f'{self.name}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
