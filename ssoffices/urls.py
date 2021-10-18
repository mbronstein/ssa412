from django.urls import path

from ss411.ssoffices import views

app_name = 'ssoffices'

urlpatterns = [
    path('', views.SsOfficeListView.as_view(), name='list'),
    path('<slug:slug>/', views.SsOfficeDetailView.as_view(), name='detail'),
]


