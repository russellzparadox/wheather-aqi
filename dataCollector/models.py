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
