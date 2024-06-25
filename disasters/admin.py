from django.contrib import admin
from .models import DisasterEvent, Report, Resource

admin.site.register(DisasterEvent)
admin.site.register(Report)
admin.site.register(Resource)
