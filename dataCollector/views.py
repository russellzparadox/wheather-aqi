from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.templatetags.rest_framework import data

from dataCollector.models import DataCollector
from dataCollector.serializer import DataCollectorSerializer

import jdatetime
from datetime import datetime, timedelta


def persian_to_django_date(persian_date_str):
    if persian_date_str == None:
        return None
    # Split the date and time parts
    date_part, time_part = persian_date_str.split()

    # Parse the date and time parts
    year, month, day = map(int, date_part.split('/'))
    hour, minute = map(int, time_part.split(':'))

    # Create a jdatetime object
    persian_date = jdatetime.datetime(year, month, day, hour, minute)

    # Convert to Gregorian datetime
    gregorian_date = persian_date.togregorian()
    # fix time zone
    gregorian_date -= timedelta(hours=3, minutes=30)

    # Format the datetime object in Django's default datetime format
    django_date_str = gregorian_date.strftime('%Y-%m-%d %H:%M:%S')

    return django_date_str


# Create your views here.
class DataCollectionCreateView(CreateAPIView):
    queryset = DataCollector.objects.all()
    serializer_class = DataCollectorSerializer

    # permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Set the logged-in user as the author of the post
        print(self.request.data)
        serializer.save()


def index(request):
    start_date = persian_to_django_date(request.GET.get('start_date', None))
    end_date = persian_to_django_date(request.GET.get('end_date', None))
    items = DataCollector.objects.order_by('id')[:100]
    attribute_names = DataCollector._meta.get_fields()
    attribute_names = attribute_names[5:]
    atr = []
    for attr in attribute_names:
        atr.append(attr.attname)
    # attribute_names = ['Humidity', 'Temperature', 'Pressure']  # Add other attribute names as needed
    attribute_names = atr
    # Initialize a dictionary to hold processed data
    processed_data = {
        'labels': [item.created_at for item in items],
        'datasets': {attr: [getattr(item, attr) for item in items] for attr in attribute_names}
    }
    print(processed_data['datasets']['Humidity'])

    if not (start_date == None or end_date == None):
        items = DataCollector.objects.filter(created_at__range=(start_date, end_date)).order_by('id')
    humidity = DataCollector.objects.values_list('Humidity', flat=True)
    data = {'data': items, 'start_date': request.GET.get('start_date', None),
            'end_date': request.GET.get('end_date', None), 'all_item': attribute_names, 'humidity': humidity,
            'processed_data': processed_data['datasets']}
    return render(request, "index.html", data)
