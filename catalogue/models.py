from django.db import models
from django.urls import reverse
from django.db.models.deletion import CASCADE


class Category(models.Model):
    """ Category Model """
    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ('-name',)
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse(
            'catalogue:product_list_by_category',
            args=[self.slug]
        )
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    """ Product Details Model """
    category = models.ForeignKey(
        Category,
        related_name = 'products',
        on_delete = models.CASCADE
    )

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('-name',)
    
    def get_absolute_url(self):
        return reverse(
            'catalogue:product_detail',
            args=[self.category.slug, self.slug]
        )
