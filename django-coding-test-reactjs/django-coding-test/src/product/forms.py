# product/forms.py
from django.forms import CheckboxInput, ModelForm, Textarea, TextInput
from product.models import Product, ProductVariantPrice, Variant


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = "__all__"
        widgets = {
            "title": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "active": CheckboxInput(
                attrs={"class": "form-check-input", "id": "active"}
            ),
        }


class ProductEditForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class ProductVariantPriceEditForm(ModelForm):
    class Meta:
        model = ProductVariantPrice
        exclude = [
            "product",
        ]


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class ProductVariantPriceForm(ModelForm):
    class Meta:
        model = ProductVariantPrice
        fields = "__all__"
