from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView
class HomeView(LoginRequiredMixin, View):
    #users = User.objects.all()
    def get(self, request):
        return render(request, 'homeapp/main.html')

class UserListView(ListView):
    model = User
    template_name = "homeapp/user_list.html"

    def get(self, request):
        # strval = request.GET.get("search", False)
        # if strval:
        #     # Simple title-only search
        #     # objects = Post.objects.filter(title__contains=strval).select_related().distinct().order_by('-updated_at')[:10]
        #
        #     # Multi-field search
        #     # __icontains for case-insensitive search
        #     query = Q(title__icontains=strval)
        #     query.add(Q(text__icontains=strval), Q.OR)
        #     ad_list = Ad.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        # else:
        #     ad_list = Ad.objects.all().order_by('-updated_at')[:10]
        #
        # # Augment the post_list
        # for obj in ad_list:
        #     obj.natural_updated = naturaltime(obj.updated_at)
        #
        # favorites = list()
        # if request.user.is_authenticated:
        #     # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
        #     rows = request.user.favorite_ads.values('id')
        #     # favorites = [2, 4, ...] using list comprehension
        #     favorites = [row['id'] for row in rows]
        user_list = User.objects.all()[:10]
        ctx = {'user_list': user_list}
        return render(request, self.template_name, ctx)