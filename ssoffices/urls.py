from django.urls import path
import ssoffices.views
from .views import ssoffice_list, SsOfficeListView, SsOfficeUpdateView
from django.contrib import admin

app_name = 'ssoffices'



urlpatterns = [
    path('offices', SsOfficeListView.as_view(), name='list'),
    path('<slug:slug>/', SsOfficeUpdateView.as_view(), name='update'),
]


# admin.site.site_header = 'LOMB Admin'
