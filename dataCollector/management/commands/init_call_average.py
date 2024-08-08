from django.core.management.base import BaseCommand
from django.db.models import Avg, Min
from dataCollector.models import DataCollector, HourlyAverage
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Calculates and logs the hourly average of data from the beginning of the data till now"

    def handle(self, *args, **kwargs):
        now = timezone.now().replace(minute=0, second=0, microsecond=0)

        # Determine the earliest created_at time in the DataCollector table
        earliest_entry = DataCollector.objects.aggregate(min_created_at=Min('created_at'))
        start_time = earliest_entry['min_created_at']

        if not start_time:
            print("No data available in the DataCollector table.")
            return

        start_time = start_time.replace(minute=0, second=0, microsecond=0)

        # Loop through each hour from start_time to now
        current_time = start_time
        while current_time <= now:
            next_hour = current_time + timedelta(hours=1)
            average_data_query = DataCollector.objects.filter(
                created_at__gte=current_time, created_at__lt=next_hour
            )

            if average_data_query.exists():
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
                    HourlyAverage.objects.create(
                        created_at=current_time,
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
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print(f"No data for the hour starting at {current_time}")

            current_time = next_hour

        print("Hourly averages calculated and logged successfully.")
