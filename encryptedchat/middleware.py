from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from homeapp.models import Profile

class UpdateLastSeenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(username=request.user.username)
            profile.update_last_seen()
            profile.is_online = True
            profile.save()

class MarkInactiveMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(username=request.user.username)
            last_seen = profile.last_seen
            if last_seen is not None and timezone.now() - last_seen > timezone.timedelta(minutes=5):
                profile.is_online = False
                profile.save()

