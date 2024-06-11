from rest_framework import serializers

from dataCollector.models import DataCollector


class DataCollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataCollector
        fields = ['Lat', 'Lng', 'Humidity', 'Temperature', 'CO', 'H2',
                  'LPG', 'CH4', 'NOx', 'CL2', 'Alchohol', 'CO2', 'Toluen',
                  'NH4', 'Aceton', 'PM1_0', 'PM2_5', 'PM10', 'device']
        read_only_fields = ['device']

    def create(self, validated_data):
        request = self.context.get('request')
        # dev = request['data']
        # dev = validated_data.get('device')
        datacollector = DataCollector.objects.create(
            # device=dev,
            Lat=validated_data['Lat'],
            Lng=validated_data['Lng'],
            Humidity=validated_data['Humidity'],
            Temperature=validated_data['Temperature'],
            CO=validated_data['CO'],
            H2=validated_data['H2'],
            LPG=validated_data['LPG'],
            CH4=validated_data['CH4'],
            NOx=validated_data['NOx'],
            CL2=validated_data['CL2'],
            Alchohol=validated_data['Alchohol'],
            CO2=validated_data['CO2'],
            Toluen=validated_data['Toluen'],
            NH4=validated_data['NH4'],
            Aceton=validated_data['Aceton'],
            PM1_0=validated_data['PM1_0'],
            PM2_5=validated_data['PM2_5'],
            PM10=validated_data['PM10'],

        )
        return datacollector
