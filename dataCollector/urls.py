from django.urls import path

from dataCollector.views import DataCollectionCreateView, index, update_map

urlpatterns = [
    path('collect/', DataCollectionCreateView.as_view(), name='index'),
    path('get-latest-data/', update_map, name='get_latest_data'),

    path('', index, name='indexView')
]
