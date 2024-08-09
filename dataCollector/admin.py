from django.contrib import admin
from dataCollector.models import DataCollector
from import_export import resources


class DataCollectorResource(resources.ModelResource):
    class Meta:
        model = DataCollector
        fields = ['Lat', 'Lng', 'Humidity', 'Temperature', 'CO', 'H2',
                  'LPG', 'CH4', 'NOx', 'CL2', 'Alchohol', 'CO2', 'Toluen',
                  'NH4', 'Aceton', 'PM1_0', 'PM2_5', 'PM10', 'device']
        # export_order = ('id', 'name')

    pass


# Register your models here.
admin.site.register(DataCollector)
