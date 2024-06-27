import os
import sys
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import JsonResponse
from django.urls import path
from django.core.management import call_command

# Add the Django app to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_management.settings')

# Initialize Django
django.setup()

# Define a simple view to test database access
from disaster_management.models import DisasterEvent 

def get_data(request):
    # Example query to get all entries from YourModel
    data = list(DisasterEvent.objects.all().values())
    return JsonResponse({'data': data})

# Define URL patterns
urlpatterns = [
    path('api/index.py', get_data),
]

# Set up Django application
application = get_wsgi_application()

# Custom WSGI handler
class DjangoWSGIApplication(django.core.handlers.wsgi.WSGIHandler):
    def __call__(self, environ, start_response):
        request = self.request_class(environ)
        response = self.get_response(request)
        if request.path == '/api/index.py':
            response = get_data(request)
        return response(environ, start_response)

# Instantiate the custom WSGI application
app = DjangoWSGIApplication()
