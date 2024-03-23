---

### Project Overview:

A project for social networking application using django restframework

### What I Did:
 
### How I Made It Happen:

- **Technology Used:**
- I used Django and Django REST Framework.
- sqlite3 as database
- JWT for Authentication
- Git and Docker
  
- **Testing and Notes:**
   - Checked everything was working using a tool called Postman.
   - Wrote down all the steps in a document so others can understand and use it later.


Installation process 



---

## Project Structure

The project is structured as follows:

- `accuknow/` - Project folder
- `app/` - Django app for management


## Setup Instructions

### 1. Create Virtual Environment

```
    python -m venv myvenv
```

### 2. Activate Virtual Environment

```
    myvenv\scripts\activate
```

### 3. Install Dependencies

Install required packages using pip:

```
    pip install django djangorestframework rest_framework-simplejwt 
```

### 4. Create Django Project and App

```
    django-admin startproject accuknox
    django-admin startapp app
```

### 5. Configuration

#### Update `settings.py`

Add the following apps to `INSTALLED_APPS` in `accuknox/settings.py`:

```
    INSTALLED_APPS = [
        # ...
      'app',
      'rest_framework',
      'rest_framework_simplejwt',
      'rest_framework_simplejwt.token_blacklist',
        # ...
    ]
```

### 6. rest_framework Configuration
```
REST_FRAMEWORK = {

        'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ],
 
    'DEFAULT_AUTHENTICATION_CLASSES': (
    
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),

      'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'app.throttle.FriendRequestThrottle',

    ],
        'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        "friend_requests": '5/minute', # throttle limit per minute
    }
}
```
### 6. URL Configuration
```

from django.urls import path,include
from .views import MytokenobtainpairView,LogoutView,FriendsView,UsersView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('friends',FriendsView,basename='friends')
router.register('users',UsersView,basename='users')

urlpatterns = [
    path('',include(router.urls)),
    path('token/', MytokenobtainpairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


```

### 7. Database Setup

Run Django migrations to set up the database:

```
    python manage.py makemigrations
    python manage.py migrate
```

### Throttle for limiting friend request 
```
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
```

### 8. Run Development Server

Start the development server:

```
    python manage.py runserver
```

### 9. Docker-compose yml
```
version: '3'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"

```
