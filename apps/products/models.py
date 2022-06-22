from django.db import models

from django.conf import settings
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    class Meta:
        app_label = "products"
        ordering = ["title"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, blank=True)
    price = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    user = models.CharField(max_length=128, default="user1")
    uploaded_by = models.CharField(max_length=128, default="admin")


    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{self.title}({self.id})"

    def get_absolute_url(self):
        return reverse('products.products', kwargs={'id': self.id})
