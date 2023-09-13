from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Chat,Message
from .serializers import ChatSerializer



class ChatList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chat/chat_list.html'

    def get(self, request):
        chats = Chat.objects.all()
        users= User.objects.all()
        return Response({'chats': chats,'users': users})



class TransactionsTemplateHTMLRender(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        data = super().get_template_context(data, renderer_context)
        if not data:
            return {}
        else:
            return data



class ChatCreateView(APIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    renderer_classes = [TransactionsTemplateHTMLRender]
    template_name = 'chat/create_chat.html'

    def get(self,requests):
        serializer=ChatSerializer()
        return Response({'serializer':serializer})

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer':serializer})
        serializer.save()
        return redirect('chat_list')


class ChatDetailView(APIView):
    renderer_classes = [TransactionsTemplateHTMLRender]
    template_name = 'chat/chat_detail.html'

    def get(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk)
        serializer = ChatSerializer(chat)
        messages = Message.objects.filter(chat=chat)[0:25]
        return Response({'serializer': serializer, 'chat': chat,'messages': messages})


class ChatUpdateView(APIView):
    renderer_classes = [TransactionsTemplateHTMLRender]
    template_name = 'chat/chat_update.html'

    def get(self,requests,pk):
        chat = get_object_or_404(Chat, pk=pk)
        serializer=ChatSerializer()
        return Response({'serializer':serializer,'chat': chat})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        instance = Chat.objects.get(pk=pk)
        serializer = ChatSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('chat_list')


class ChatDeleteView(APIView):
    renderer_classes = [TransactionsTemplateHTMLRender]
    queryset = Chat.objects.all()
    template_name = 'chat/chat_delete.html'

    def get(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk)
        serializer = ChatSerializer(chat)
        return Response({'serializer': serializer, 'chat': chat})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        instance = Chat.objects.get(pk=pk)
        instance.delete()
        return redirect('chat_list')

