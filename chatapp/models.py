from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from homeapp.models import Profile

class Message(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(1, "Message must be greater than 1 character")]
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    chat = GenericForeignKey('content_type', 'object_id')

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15: return self.text
        return self.text[:11] + ' ...'

class PrivateChat(models.Model):
    participants = models.ManyToManyField(Profile, related_name='chat_participants')

    messages = GenericRelation(Message)

    # Shows up in the admin list
    def __str__(self):
        participants_usernames = ', '.join([participant.username for participant in self.participants.all()])
        return f"Private chat: {participants_usernames}"

class GroupChat(PrivateChat):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 1 character")]
    )
    # Picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    # Shows up in the admin list
    def __str__(self):
        return f"Group chat: {self.title}"