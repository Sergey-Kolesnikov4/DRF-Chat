from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from .forms import RegisterForm,ProfileUpdateForm
from django.views import View
from django.views.generic import ListView
from .models import Profile

def home(request):
    return render(request,'home.html')

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
            
        return super(RegisterView, self).form_valid(form)
    
    
class MyLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('profile')
    
    def form_invalid(self, form):
        messages.error(self.request,'Неверное имя пользователя или пароль')
        return self.render_to_response(self.get_context_data(form=form))


class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
        context = {
            'profile_form': profile_form
        }
        
        return render(request, 'users/profile.html', context)
    
    def post(self,request):
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if profile_form.is_valid():
            profile_form.save()
            
            messages.success(request,'Ваш профиль был успешно обновлен')
            
            return redirect('profile')
        else:
            context = {
                'profile_form': profile_form
            }
            messages.error(request,'Ошибка при обновлении вашего профиля')
            
            return render(request, 'users/profile.html', context)


class ProfileList(ListView):
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'Profiles'