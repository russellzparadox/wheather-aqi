from django.urls import path

from view.views import index

urlpatterns = [
    path('', index, name='indexView')
]
