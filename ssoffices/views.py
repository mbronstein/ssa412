from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone


from ss411.ssoffices.models import SsOffice

class SsOfficeListView(ListView):
    model=SsOffice   # this is shortcut for setting queryset = SsOffice.objects.all()
    paginate_by = 100  # if pagination is desired
    template_name = "ssoffices/ssoffice_list.html"
    context_object_name = 'ssoffices'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context


class SsOfficeDetailView(DetailView):
    model = SsOffice  # this is shortcut for setting queryset = SsOffice.objects.all()
    template_name = 'ssoffices/ssoffice_detail.html'
    context_object_name = 'selected ssoffice'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context
    #
    # def get_queryset(self):
    #     return SsOffice.objects.all()
