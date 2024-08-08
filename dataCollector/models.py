from django.db import models
from django_jalali.db import models as jmodels


class Device(models.Model):
    sn = models.CharField(max_length=256)


# Create your models here.
class DataCollector(models.Model):
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    # cr_at_jl = jmodels.jDateTimeField(auto_now=True)
    device = models.ForeignKey(Device, null=True, on_delete=models.SET_NULL)
    Lat = models.FloatField()
    Lng = models.FloatField()
    Humidity = models.FloatField()
    Temperature = models.FloatField()
    CO = models.FloatField()
    H2 = models.FloatField()
    LPG = models.FloatField()
    CH4 = models.FloatField()
    NOx = models.FloatField()
    CL2 = models.FloatField()
    Alchohol = models.FloatField()
    CO2 = models.FloatField()
    Toluen = models.FloatField()
    NH4 = models.FloatField()
    Aceton = models.FloatField()
    PM1_0 = models.FloatField()
    PM2_5 = models.FloatField()
    PM10 = models.FloatField()


class HourlyAverage(models.Model):
    device = models.ForeignKey(Device, null=True, on_delete=models.SET_NULL)
    created_at = jmodels.jDateTimeField(unique=True)
    Lat = models.FloatField()
    Lng = models.FloatField()
    aqi = models.FloatField(null=True)
    Humidity = models.FloatField()
    Temperature = models.FloatField()
    CO = models.FloatField()
    H2 = models.FloatField()
    LPG = models.FloatField()
    CH4 = models.FloatField()
    NOx = models.FloatField()
    CL2 = models.FloatField()
    Alchohol = models.FloatField()
    CO2 = models.FloatField()
    Toluen = models.FloatField()
    NH4 = models.FloatField()
    Aceton = models.FloatField()
    PM1_0 = models.FloatField()
    PM2_5 = models.FloatField()
    PM10 = models.FloatField()

    AQI_BREAKPOINTS = {
        'PM2_5': [
            {'low': 0, 'high': 12, 'aqi_low': 0, 'aqi_high': 50},
            {'low': 12.1, 'high': 35.4, 'aqi_low': 51, 'aqi_high': 100},
            # ... more breakpoints ...
        ],
        'PM10': [
            {'low': 0, 'high': 54, 'aqi_low': 0, 'aqi_high': 50},
            {'low': 55, 'high': 154, 'aqi_low': 51, 'aqi_high': 100},
            # ... more breakpoints ...
        ],
        'CO': [
            {'low': 0, 'high': 4.4, 'aqi_low': 0, 'aqi_high': 50},
            {'low': 4.5, 'high': 9.4, 'aqi_low': 51, 'aqi_high': 100},
            # ... more breakpoints ...
        ],
        'NOx': [
            {'low': 0, 'high': 53, 'aqi_low': 0, 'aqi_high': 50},
            {'low': 54, 'high': 100, 'aqi_low': 51, 'aqi_high': 100},
            # ... more breakpoints ...
        ],
        # Add other pollutants if needed
    }

    def calculate_aqi_for_pollutant(self, concentration, breakpoints):
        for bp in breakpoints:
            if bp['low'] <= concentration <= bp['high']:
                return ((bp['aqi_high'] - bp['aqi_low']) / (bp['high'] - bp['low'])) * (concentration - bp['low']) + bp[
                    'aqi_low']
        return None  # Handle out-of-range values appropriately

    def calculate_aqi(self):
        data = {
            'PM2_5': self.PM2_5,
            'PM10': self.PM10,
            'CO': self.CO,
            'NOx': self.NOx,
            # Add other pollutants if needed
        }
        aqi_values = []

        for pollutant, concentration in data.items():
            if pollutant in self.AQI_BREAKPOINTS:
                aqi = self.calculate_aqi_for_pollutant(concentration, self.AQI_BREAKPOINTS[pollutant])
                if aqi is not None:
                    aqi_values.append(aqi)

        if aqi_values:
            return max(aqi_values)
        return None  # or some default value, e.g., 0 or "No Data"
