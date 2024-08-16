import json

import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from sklearn.neighbors import NearestNeighbors

from dataCollector.models import DataCollector
from dataCollector.serializer import DataCollectorSerializer
from dataCollector.utils import persian_to_django_date


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
    start_date = persian_to_django_date(request.GET.get("start_date", None))
    end_date = persian_to_django_date(request.GET.get("end_date", None))
    items = DataCollector.objects.order_by("-id")[:80]
    items = items[::-1]
    attribute_names = DataCollector._meta.get_fields()
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
        items = DataCollector.objects.filter(
            created_at__range=(start_date, end_date)
        ).order_by("id")
    humidity = DataCollector.objects.values_list("Humidity", flat=True)
    data = {
        "data": items,
        "start_date": request.GET.get("start_date", None),
        "end_date": request.GET.get("end_date", None),
        "all_item": attribute_names,
        "humidity": humidity,
        "processed_data": processed_data["datasets"],
    }
    return render(request, "index.html", data)


# def idk(request):
#     latitude = 10.12333333345678
#     longitude = 10.12333333345678
#     k = 5
#
#     # Fetch all data points from the database
#     data = list(DataCollector.objects.all().values('lat', 'lng', 'humidity'))
#
#     # Extract coordinates and values
#     coordinates = np.array([[item['lat'], item['lng']] for item in data])
#     values = np.array([item['humidity'] for item in data])  # Replace 'humidity' with the desired field
#
#     # Initialize and fit the k-NN model
#     knn = NearestNeighbors(n_neighbors=k)
#     knn.fit(coordinates)
#
#     # Find the k-nearest neighbors
#     distances, indices = knn.kneighbors([[latitude, longitude]])
#
#     # Calculate the average value of the k-nearest neighbors
#     neighbor_values = values[indices[0]]
#     average_value = np.mean(neighbor_values)
#
#     self.stdout.write(self.style.SUCCESS(f'The average value of the {k}-nearest neighbors: {average_value}'))
def update_map(request):
    dt = json.loads(request.body)
    latitude = dt.get("lat")
    longitude = dt.get("lng")
    k = 3

    # Fetch all data points from the database
    dat = list(DataCollector.objects.order_by("-id")[:30].values())

    # Extract coordinates
    coordinates = np.array([[item["Lat"], item["Lng"]] for item in dat])

    # Extract attribute values
    attribute_names = [
        "Humidity",
        "Temperature",
        "CO",
        "H2",
        "LPG",
        "CH4",
        "NOx",
        "CL2",
        "Alchohol",
        "CO2",
        "Toluen",
        "NH4",
        "Aceton",
        "PM1_0",
        "PM2_5",
        "PM10",
    ]
    attribute_values = {
        name: np.array([item[name] for item in dat]) for name in attribute_names
    }

    # Initialize and fit the k-NN model
    knn = NearestNeighbors(n_neighbors=k)
    knn.fit(coordinates)

    # Find the k-nearest neighbors
    distances, indices = knn.kneighbors([[latitude, longitude]])

    # Calculate the average value of the k-nearest neighbors for each attribute
    average_values = {}
    for name in attribute_names:
        neighbor_values = attribute_values[name][indices[0]]
        average_values[name] = np.mean(neighbor_values)
    rounded_average_values = {
        key: round(value, 2) for key, value in average_values.items()
    }
    print(average_values)
    # Print the average values
    # for name, avg in average_values.items():
    #     self.stdout.write(self.style.SUCCESS(f'The average {name} value of the {k}-nearest neighbors: {avg}'))

    return JsonResponse(rounded_average_values)
