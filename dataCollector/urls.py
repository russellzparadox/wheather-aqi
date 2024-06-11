from django.urls import path

from dataCollector.views import DataCollectionCreateView, index

urlpatterns = [
    path('collect/', DataCollectionCreateView.as_view(), name='index'),
    path('', index, name='indexView')
]
