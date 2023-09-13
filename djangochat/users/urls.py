from django.urls import path
from .views import MyLoginView, RegisterView, MyProfile,home,ProfileList



from django.contrib.auth.views import (
    LogoutView,
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', MyLoginView.as_view(redirect_authenticated_user=True),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', RegisterView.as_view(),name='register'),
    path('profile/', MyProfile.as_view(), name='profile'),
    path('profile_list/', ProfileList.as_view(), name='profile_list'),
]



