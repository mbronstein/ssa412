from django.urls import path
from .views import SsOfficeListView, SsOfficeUpdateView

app_name = 'ssoffices'



urlpatterns = [
    path('offices', SsOfficeListView.as_view(), name='list'),
    path('<slug:slug>/', SsOfficeUpdateView.as_view(), name='update'),
]


# admin.site.site_header = 'LOMB Admin'
