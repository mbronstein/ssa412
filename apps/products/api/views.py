from rest_framework.viewsets import ModelViewSet
from apps.products.models import Product
from apps.products.api.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

