from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"events", views.DisasterEventViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'resources', views.ResourceViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("event/<int:event_id>/", views.event_detail,name="event_detail"),
    path("register/", views.register, name = "register"),
    path("api/", include(router.urls)),
    path('create_event/', views.create_event, name='create_event'),
    path('report_event/', views.report_event, name='report_event'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  
    path('submit_resource/', views.submit_resource, name='submit_resource'),
    path('search/', views.search_events, name='search_events'),
    path('register/', views.register, name='register'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('events/', views.events_list, name='events_list'),
    path('event-dashboard/', views.event_dashboard, name='event_dashboard'),
    path('api/event-data/', views.get_event_data, name='get_event_data'),
]
