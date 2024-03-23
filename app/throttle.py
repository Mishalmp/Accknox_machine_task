from django.core.cache import cache
from rest_framework.throttling import BaseThrottle
from django.utils import timezone

class FriendRequestThrottle(BaseThrottle):
    def allow_request(self, request, view):
        user = request.user
        throttle_limit = 3  # No of requests allowed
        throttle_period = 60  # Throttle period
        # Generate a unique key for caching friend requests based on user ID
        cache_key = f"friend_requests_{user.id}"
        previous_requests = cache.get(cache_key, [])
        # Filter out requests that are older than the throttle period
        current_time = timezone.now()
        previous_requests = [r for r in previous_requests if (current_time - r).total_seconds() <= throttle_period]

        if len(previous_requests) >= throttle_limit:
            return False

        previous_requests.append(current_time)
        cache.set(cache_key, previous_requests, throttle_period)

        return True
