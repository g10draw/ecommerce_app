from django.db import models
from catalogue.models import Product
from django.conf import settings
from django.urls import reverse

# ORDER STATUS OPTIONS
ORDER_STATUS = [
    ('Created', 'Created'),
    ('Processing', 'Processing'),
    ('Completed', 'Completed'),
    ('Payment Failed', 'Payment Failed')
]


class Order(models.Model):
    """ Order Details Model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        blank=True, 
        null=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Order Created')
    note = models.TextField(blank=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order #{self.id}'
    
    # Calculates total cost of the products in order
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    # Fetches the unique url of each order
    def get_absolute_url(self):
        return reverse(
            'orders:order_detail',
            args=[self.id]
        )


class OrderItem(models.Model):
    """ Order Item Details Model """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)
    
    # Calculates cost according to it's quantity
    def get_cost(self):
        return self.price * self.quantity