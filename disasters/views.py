from django.shortcuts import render,redirect,get_object_or_404
from .models import DisasterEvent, Report, Resource
from .forms import ReportForm, ResourceForm,DisasterEventForm, CustomUserCreationForm,UserProfile
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from .serializers import DisasterEventSerializer, ReportSerializer, ResourceSerializers
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import send_sms
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import Lower



class DisasterEventViewSet(viewsets.ModelViewSet):
    queryset = DisasterEvent.objects.all()
    serializer_class = DisasterEventSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializers

def index(request):
    query = request.GET.get('q', '')
    events = DisasterEvent.objects.filter(name__icontains=query) if query else []
    return render(request, 'disasters/index.html', {'events': events, 'query': query})
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(DisasterEvent, id=event_id)
    reports = event.report_set.all()
    resources = event.resource_set.all()
    
    if request.method == 'POST':
        if 'report_submit' in request.POST:
            report_form = ReportForm(request.POST)
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.event = event
                report.save()
                return redirect('event_detail', event_id=event.id)
        elif 'resource_submit' in request.POST:
            resource_form = ResourceForm(request.POST)
            if resource_form.is_valid():
                resource = resource_form.save(commit=False)
                resource.event = event
                resource.save()
                return redirect('event_detail', event_id=event.id)
    else:
        report_form = ReportForm(initial={'event': event})
        resource_form = ResourceForm(initial={'event': event})
    
    return render(request, 'disasters/event_detail.html', {
        'event': event,
        'reports': reports,
        'resources': resources,
        'report_form': report_form,
        'resource_form': resource_form,
    })
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'disasters/register.html', {'form': form})

@login_required
# @user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Admin').exists())
def create_event(request):
    if request.method == "POST":
        form = DisasterEventForm(request.POST)
        if form.is_valid():
            event = form.save()
            # Send SMS notification
            message = f'A new disaster event "{event.name}" has been created.\n\nDetails:\nEvent Type: {event.event_type}\nLocation: {event.location}\nDate Occurred: {event.date_occurred}\nDescription: {event.description}'
            recipient_number = request.user.userprofile.phone_number  
            if recipient_number:
                send_sms(recipient_number, message)
            return redirect('index')
    else:
        form = DisasterEventForm()
    return render(request, 'disasters/create_event.html', {'form': form})

@login_required
def report_event(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ReportForm()
    return render(request, 'disasters/report_event.html', {'form': form})

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def admin_dashboard(request):
    events_count = DisasterEvent.objects.count()
    reports_count = Report.objects.count()
    resources_count = Resource.objects.count()
    return render(request, 'disasters/admin_dashboard.html', {
        'events_count': events_count,
        'reports_count': reports_count,
        'resources_count': resources_count,
    })

@login_required
def submit_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.available = True  # Automatically set the available field to True
            resource.save()
            return redirect('index')
    else:
        form = ResourceForm()
    return render(request, 'disasters/submit_resource.html', {'form': form})
def search_events(request):
    query = request.GET.get("q")
    event_type = request.GET.get("event_type")
    events = DisasterEvent.objects.all()
    if query:
        events = events.filter(name__icontains=query)
    if event_type:
        events = events.filter(event_type=event_type)

    return render(request, 'disasters/search_events.html', {'events': events})
    
@login_required
def view_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'disasters/view_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = CustomUserCreationForm(instance=profile)
    return render(request, 'disasters/edit_profile.html', {'form': form})

def events_list(request):
    events= DisasterEvent.objects.all()
    return render(request, 'disasters/events_list.html', {'events': events})
@login_required
def event_dashboard(request):
    cities= DisasterEvent.objects.values("location").annotate(event_count=Count("id"))
    city_labels = [city['location'] for city in cities]
    event_counts = [city['event_count'] for city in cities]
    return render(request, 'disasters/event_dashboard.html', {
        'city_labels': city_labels,
        'event_counts': event_counts,
    })

def get_event_data(request):
    search_query = request.GET.get('search', '').lower()
    
    if search_query:
        events = DisasterEvent.objects.annotate(
            lower_name=Lower('name')
        ).filter(lower_name__contains=search_query)
    else:
        events = DisasterEvent.objects.all()

    event_counts = events.values('location').annotate(count=Count('id')).order_by('location')
    
    labels = [event['location'] for event in event_counts]
    data = [event['count'] for event in event_counts]
    
    event_counts_by_type = events.values('event_type').annotate(count=Count('id')).order_by('event_type')
    
    labels_type = [event['event_type'] for event in event_counts_by_type]
    data_type = [event['count'] for event in event_counts_by_type]

    return JsonResponse({
        'location': {'labels': labels, 'data': data},
        'type': {'labels': labels_type, 'data': data_type},
    })

def event_type_data(request):
    event_types = DisasterEvent.objects.all()
    labels = [event_type.name for event_type in event_types]
    counts = [event_type.event_set.count() for event_type in event_types]
    data = {
        'labels': labels,
        'counts': counts,
    }
    return JsonResponse(data)