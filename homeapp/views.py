from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import RegistrationForm

from django.views.generic import ListView, DetailView
class HomeView(View):
    def get(self, request):
        return render(request, 'homeapp/main.html')

class ProfileListView(View):
    template_name = "homeapp/profile_list.html"
    def get(self, request):
        input = request.session.get('input', False)
        if (input): 
            del(request.session['input'])
            profiles = Profile.objects.filter(username__icontains=input)
            search = True
        else:
            profiles = Profile.objects.all()
            search = False

        return render(request, self.template_name, {'profiles': profiles, 'search': search})
    
    def post(self, request):
        input = request.POST.get('input')
        if input:
            request.session['input'] = input
        
        return redirect(request.path)
    
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'homeapp/profile_detail.html'
    context_object_name = 'profile'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
