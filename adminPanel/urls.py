from django.urls import path

from adminPanel.views import index, login_view, logout_view, DataCollectorListView, redirectView

urlpatterns = [
    path('', redirectView, name='index'),
    path('table/<str:att>/', index, name='admin-index'),
    path('login/', login_view, name='admin-login'),
    path('logout/', logout_view, name='admin-logout'),
    path('export/', DataCollectorListView.as_view(), name='admin-export-datacollector-list'),
    # path('', url=reverse_lazy('admin-login'), permanent=True),

]
