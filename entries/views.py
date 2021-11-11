from wip.entries.models import Entry
# from .serializers import EntrySerializer
from rest_framework import viewsets

class EntryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Entry.objects.all()
    # serializer_class = EntrySerializer
