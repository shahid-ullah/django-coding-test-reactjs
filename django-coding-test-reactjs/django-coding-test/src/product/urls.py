# product/urls.py
from django.urls import path
from product.views.product import (ProductListView, product_create_view,
                                   product_edit_view,
                                   product_variant_price_edit_view)
from product.views.variant import (VariantCreateView, VariantEditView,
                                   VariantView)

app_name = "product"

urlpatterns = [
    # Variants URLs
    path("variants/", VariantView.as_view(), name="variants"),
    path("variant/create", VariantCreateView.as_view(), name="create.variant"),
    path("variant/<int:id>/edit", VariantEditView.as_view(), name="update.variant"),
    # Products URLs
    # path("create/", CreateProductView.as_view(), name="create.product"),
    path("create/", product_create_view, name="create.product"),
    path("<int:id>/edit/", product_edit_view, name="edit.product"),
    path(
        "<int:id>/edit_pvc/",
        product_variant_price_edit_view,
        name="edit.product_variant_price",
    ),
    # path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
    #     'product': True
    # }), name='list.product'),
    path("list/", ProductListView.as_view(), name="list.product"),
]
