from django.shortcuts import get_object_or_404, render

from .models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    """ Fetches products pased on selected category """
    categories = Category.objects.all()
    requested_category = None
    products = Product.objects.all()

    # Filter products by category
    if category_slug:
        requested_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=requested_category)

    return render(
        request,
        'product/list.html',
        {
            'categories': categories,
            'requested_category': requested_category,
            'products': products
        }
    )

def product_detail(request, category_slug, product_slug):
    """ Handles product details page """
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(
        Product,
        category_id=category.id,
        slug=product_slug
    )
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
        }
    )