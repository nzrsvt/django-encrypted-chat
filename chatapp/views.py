from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from .models import Message, PrivateChat, GroupChat

# Create your views here.
class PrivateChatView(LoginRequiredMixin, View):
    template_name = "chatapp/private_chat.html"
    def get(self, request, pk):
        interlocutor = get_object_or_404(User, id=pk)

        private_chat = PrivateChat.objects.filter(participants=request.user).filter(participants=interlocutor).first()

        if not private_chat:
            private_chat = PrivateChat.objects.create()
            private_chat.participants.add(request.user, interlocutor)

        messages = Message.objects.filter(
            content_type=ContentType.objects.get_for_model(private_chat),
            object_id=private_chat.id
        )

        ctx = {'user': request.user, 'interlocutor': interlocutor, 'messages': messages, 'chat_id': private_chat.id}

        return render(request, self.template_name, ctx)
    def post(self, request, pk) :
        m = get_object_or_404(Message, id=pk)
        m.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])