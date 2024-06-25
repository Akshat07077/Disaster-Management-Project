import os
import sys

# Adjust the path to your Django app
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_management.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
