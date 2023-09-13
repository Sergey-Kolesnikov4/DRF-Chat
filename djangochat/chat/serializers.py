from .models import Chat
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ["id", "name"]

    def create(self, validated_data):
        chat=Chat.objects.create(**validated_data)
        chat.save()
        return chat

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance
