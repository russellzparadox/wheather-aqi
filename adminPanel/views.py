import pickle

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, FormView

from dataCollector.admin import DataCollectorResource
from dataCollector.forms import FormatForm, DateRangeForm
from dataCollector.models import DataCollector
from dataCollector.views import persian_to_django_date


class DataCollectorListView(ListView, FormView):
    model = DataCollector
    template_name = "admin/main.html"
    form_class = FormatForm
    context_object_name = 'data_collectors'
    paginate_by = 25  # Load 20 records per page (adjust as needed)
    date_form_class = DateRangeForm

    def post(self, request, *args, **kwargs):
        qs = self.get_queryset()
        dataset = DataCollectorResource().export(qs)
        format = request.POST.get('format')
        if format == 'xls':
            ds = dataset.export('xls')
        elif format == 'csv':
            ds = dataset.export('csv')
        elif format == 'json':
            ds = dataset.export('json')
        response = HttpResponse(ds, content_type=f'{format}')
        response['Content-Disposition'] = f'attachment; filename="DataCollector.{format}"'
        return response

    # def get(self, request, *args, **kwargs):
    def get_queryset(self):
        qs = DataCollector.objects.select_related('device').order_by('-created_at')
        start_date = self.request.GET.get('start_date', None)
        # start_date =
        end_date = self.request.GET.get('end_date', None)
        if start_date and end_date:
            start_date = persian_to_django_date(start_date)
            end_date = persian_to_django_date(end_date)
            qs = qs.filter(created_at__range=[start_date, end_date])

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attribute_names = DataCollector._meta.get_fields()
        attribute_names = attribute_names[5:]
        atr = []
        for attr in attribute_names:
            atr.append(attr.attname)
        attribute_names = atr

        # Include DateRangeForm in the context
        context['date_form'] = self.date_form_class(self.request.GET or None)
        context['attribute_names'] = attribute_names
        return context


def index(request, att):
    attribute_names = DataCollector._meta.get_fields()
    attribute_names = attribute_names[5:]
    atr = []
    for attr in attribute_names:
        atr.append(attr.attname)
    attribute_names = atr
    att_name = att
    if not request.user.is_authenticated or not request.user.is_superuser or not request.user.is_staff:
        return redirect('admin-login')
    data = dict()
    query_set = DataCollector.objects.values_list(att_name, 'created_at')
    reloaded_query_set = DataCollector.objects.all()
    reloaded_query_set.query = pickle.loads(pickle.dumps(query_set.query))
    print(reloaded_query_set)
    rawData = reloaded_query_set.values_list(att, flat=True)
    data['user'] = request.user
    data['data'] = reloaded_query_set
    data['raw_data'] = rawData
    data['att_name'] = att_name
    data['attribute_names'] = attribute_names
    # if not request.user.is_authenticated:
    #     return redirect(reverse('admin-login'))
    return render(request, 'admin/index.html', data)


def redirectView(request):
    return redirect('admin-login')


def logout_view(request):
    logout(request)
    return redirect('admin-login')


def login_view(request):
    if request.method == "GET":
        data = dict()
        if request.user.is_authenticated:
            if request.user.is_superuser and request.user.is_staff:
                return redirect(reverse('admin-index', args=['CO']))

            return render(request, 'admin/login.html', {"error": "شما این دسترسی را ندارید"})
        return render(request, 'admin/login.html', data)
    if request.method == "POST":
        uName = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=uName, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('admin-index', args=['CO']))
        else:
            return render(request, 'admin/login.html', {"error": "نام کاربری یا کلمه عبور اشتباه است"})
