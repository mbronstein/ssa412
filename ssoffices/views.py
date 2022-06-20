from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import django_filters as filters

from django_tables2.views import SingleTableMixin
from .models import SsOffice
from django_tables2 import SingleTableView
from .tables import SsOfficeTable

# class SsOfficeListView(SingleTableView):
#     model = SsOffice
#     table_class = SsOfficeTable



class SsOfficeFilter(filters.FilterSet):
    class Meta:
        model = SsOffice
        fields = ['type', 'state', 'city']

def ssoffice_list(request):
    return render(request, 'ssoffices/ssoffice_list.html'
    )

class SsOfficeListView(SingleTableView):
    model = SsOffice
    table_class = SsOfficeTable
    template_name = 'ssoffices/ssoffice_list.html'

class SsOfficeCreateView(CreateView):
    model = SsOffice
    fields = ['__all__' ]

class SsOfficeUpdateView(UpdateView):
    model = SsOffice
    fields = ['name''__all__' ]

# class SsOfficeDeleteView(DeleteView):
#     model = SsOffice
#     success_url = reverse_lazy('author-list')



#
# class SSOficeFormView(FormView):
#     template_name = 'contact.html'
#     form_class = SsOfficeForm
#

# class SsOfficeListView(ListView):
#     model=SsOffice   # this is shortcut for setting queryset = SsOffice.objects.all()
#     paginate_by = 100  # if pagination is desired
#     template_name = "ssoffices/ssoffice_list.html"
#     context_object_name = 'ssoffices'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['now'] = timezone.now()
#     #     return context

#
# class SsOfficeDetailView(DetailView):
#     model = SsOffice  # this is shortcut for setting queryset = SsOffice.objects.all()
#     template_name = 'ssoffices/ssoffice_detail.html'
#     context_object_name = 'selected ssoffice'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context
    #
    # def get_queryset(self):
    #     return SsOffice.objects.all()
