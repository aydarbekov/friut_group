from django.core.exceptions import ValidationError
from django.forms import ModelForm

from webapp.models import Order


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone']