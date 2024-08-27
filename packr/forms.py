from .models import Item, Pack

from django import forms


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
            "name",
            "weight",
            "dimension_x",
            "dimension_y",
            "dimension_z",
            "is_bag",
        ]


class PackForm(forms.ModelForm):

    class Meta:
        model = Pack
        fields = ["name", "bag", "items"]
