from django.utils.deprecation import MiddlewareMixin
from homeapp.models import Profile

class UpdateLastSeenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(username=request.user.username)
            profile.update_last_seen()
            profile.is_online = True
            profile.save()
