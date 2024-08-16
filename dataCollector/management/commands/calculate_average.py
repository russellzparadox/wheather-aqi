from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Avg
from django.utils import timezone

from dataCollector.models import DataCollector, HourlyAverage  # Replace with your model


class Command(BaseCommand):
    help = "Calculates and logs the average of data every hour"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        now = now.replace(minute=0, second=0, microsecond=0)

        if now.minute == 0:
            # Perform the average calculation
            average_data_query = None
            count = 10
            while not average_data_query and count != 0:
                average_data_query = DataCollector.objects.filter(
                    created_at__gte=now - timedelta(hours=1), created_at__lte=now
                )
                now = now - timedelta(hours=1)
                count -= 1
            if not average_data_query:
                print("there is no data available for the pas ten hour")
                exit(0)
            average_values = average_data_query.aggregate(
                avg_lat=Avg('Lat'),
                avg_lng=Avg('Lng'),
                avg_humidity=Avg('Humidity'),
                avg_temperature=Avg('Temperature'),
                avg_co=Avg('CO'),
                avg_h2=Avg('H2'),
                avg_lpg=Avg('LPG'),
                avg_ch4=Avg('CH4'),
                avg_nox=Avg('NOx'),
                avg_cl2=Avg('CL2'),
                avg_alchohol=Avg('Alchohol'),
                avg_co2=Avg('CO2'),
                avg_toluen=Avg('Toluen'),
                avg_nh4=Avg('NH4'),
                avg_aceton=Avg('Aceton'),
                avg_pm1_0=Avg('PM1_0'),
                avg_pm2_5=Avg('PM2_5'),
                avg_pm10=Avg('PM10')
            )

            try:
                HAV = HourlyAverage.objects.create(
                    created_at=now,  # or use auto_now_add to set the current time automatically
                    Lat=average_values['avg_lat'],
                    Lng=average_values['avg_lng'],
                    Humidity=average_values['avg_humidity'],
                    Temperature=average_values['avg_temperature'],
                    CO=average_values['avg_co'],
                    H2=average_values['avg_h2'],
                    LPG=average_values['avg_lpg'],
                    CH4=average_values['avg_ch4'],
                    NOx=average_values['avg_nox'],
                    CL2=average_values['avg_cl2'],
                    Alchohol=average_values['avg_alchohol'],
                    CO2=average_values['avg_co2'],
                    Toluen=average_values['avg_toluen'],
                    NH4=average_values['avg_nh4'],
                    Aceton=average_values['avg_aceton'],
                    PM1_0=average_values['avg_pm1_0'],
                    PM2_5=average_values['avg_pm2_5'],
                    PM10=average_values['avg_pm10']
                )
                if HAV.aqi is None:
                    HAV.aqi = HAV.calculate_aqi()
                    HAV.save()
            except Exception as e:
                print(f'an error has oucored {e}')
