from django import forms
from .models import Order,Refund

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_note']
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class RefundForm(forms.ModelForm):

    class Meta:
        model = Refund
        fields = ['reason'] 