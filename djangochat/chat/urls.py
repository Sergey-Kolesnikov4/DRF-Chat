from django.urls import path

from .views import ChatList,ChatCreateView,ChatDetailView,ChatUpdateView,ChatDeleteView



urlpatterns = [
    path('chat_list/', ChatList.as_view(), name='chat_list'),
    path('create_chat/', ChatCreateView.as_view(), name='create_chat'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('<int:pk>/update/', ChatUpdateView.as_view(), name='chat_update'),
    path('<int:pk>/delete/', ChatDeleteView.as_view(), name='chat_delete'),
    ]