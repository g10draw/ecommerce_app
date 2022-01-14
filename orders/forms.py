from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Order


class OrderCreatedForm(forms.ModelForm):
    """ Delivery Information Details """
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'mobile', 
            'address', 'postal_code', 'city', 'country'
        ]

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'mobile': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'postal_code': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'city': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'country': forms.TextInput(
                attrs={'class': 'form-control'}
            )
        }