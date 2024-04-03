from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView
class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'homeapp/main.html')

class UserListView(View):
    template_name = "homeapp/user_list.html"
    def get(self, request):
        input = request.session.get('input', False)
        if (input): 
            del(request.session['input'])
            users = User.objects.filter(username__icontains=input)
            search = True
        else:
            users = User.objects.all()
            search = False

        return render(request, self.template_name, {'users': users, 'search': search})
    
    def post(self, request):
        input = request.POST.get('input')
        if input:
            request.session['input'] = input
        
        return redirect(request.path)