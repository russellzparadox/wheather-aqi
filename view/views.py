from django.shortcuts import render
from dataCollector.views import persian_to_django_date
from dataCollector.models import HourlyAverage
# Create your views here.
def index(request):
    start_date = persian_to_django_date(request.GET.get("start_date", None))
    end_date = persian_to_django_date(request.GET.get("end_date", None))
    items = HourlyAverage.objects.order_by("-id")[:30]
    items = items[::-1]
    attribute_names = HourlyAverage._meta.get_fields()
    attribute_names = attribute_names[5:]
    atr = []
    for attr in attribute_names:
        atr.append(attr.attname)
    # attribute_names = ['Humidity', 'Temperature', 'Pressure']  # Add other attribute names as needed
    attribute_names = atr
    # Initialize a dictionary to hold processed data
    processed_data = {
        "labels": [item.created_at for item in items],
        "datasets": {
            attr: [getattr(item, attr) for item in items] for attr in attribute_names
        },
    }
    print(processed_data["datasets"]["Humidity"])

    if not (start_date == None or end_date == None):
        items = HourlyAverage.objects.filter(
            created_at__range=(start_date, end_date)
        ).order_by("id")
    humidity = HourlyAverage.objects.values_list("Humidity", flat=True)
    data = {
        "data": items,
        "start_date": request.GET.get("start_date", None),
        "end_date": request.GET.get("end_date", None),
        "all_item": attribute_names,
        "humidity": humidity,
        "processed_data": processed_data["datasets"],
    }
    return render(request, "index.html", data)

