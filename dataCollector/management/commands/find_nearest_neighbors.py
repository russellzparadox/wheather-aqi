import numpy as np
from django.core.management.base import BaseCommand
from sklearn.neighbors import NearestNeighbors
from dataCollector.models import DataCollector  # Replace 'myapp' with your app name


class Command(BaseCommand):
    help = 'Find k-nearest neighbors and calculate the average values of all attributes'

    def add_arguments(self, parser):
        parser.add_argument('latitude', type=float, help='Latitude of the point')
        parser.add_argument('longitude', type=float, help='Longitude of the point')
        parser.add_argument('k', type=int, help='Number of nearest neighbors')

    def handle(self, *args, **kwargs):
        latitude = kwargs['latitude']
        longitude = kwargs['longitude']
        k = kwargs['k']

        # Fetch all data points from the database
        data = list(DataCollector.objects.all().values())

        # Extract coordinates
        coordinates = np.array([[item['Lat'], item['Lng']] for item in data])

        # Extract attribute values
        attribute_names = ['Humidity', 'Temperature', 'CO', 'H2', 'LPG', 'CH4', 'NOx', 'CL2',
                           'Alchohol', 'CO2', 'Toluen', 'NH4', 'Aceton', 'PM1_0', 'PM2_5', 'PM10']
        attribute_values = {name: np.array([item[name] for item in data]) for name in attribute_names}

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

        # Print the average values
        for name, avg in average_values.items():
            self.stdout.write(self.style.SUCCESS(f'The average {name} value of the {k}-nearest neighbors: {avg}'))
