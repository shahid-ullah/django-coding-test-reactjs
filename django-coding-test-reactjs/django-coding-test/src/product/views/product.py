# product/views/product.py
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from product.models import Product, ProductVariantPrice, Variant

from ..forms import (ProductCreateForm, ProductEditForm,
                     ProductVariantPriceEditForm)


class CreateProductView(generic.TemplateView):
    template_name = "products/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values("id", "title")
        context["product"] = True
        context["variants"] = list(variants.all())
        return context


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 4
    template_name = "products/list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context["product"] = True
        context["variants"] = Variant.objects.filter(active=True).all()
        return context

    def get_queryset(self):
        title = self.request.GET.get("title")
        date = self.request.GET.get("date")
        price_from = self.request.GET.get("price_from")
        price_to = self.request.GET.get("price_to")
        variant = self.request.GET.get("variant", "")

        queryset = super(ProductListView, self).get_queryset()
        if variant:

            variant_type, value = variant.split("_")
            if variant_type == "Size":
                queryset = queryset.filter(
                    productvariantprice__product_variant_one__variant_title=value
                ).distinct()
            elif variant_type == "Color":
                queryset = queryset.filter(
                    productvariantprice__product_variant_two__variant_title=value
                )
            elif variant_type == "Style":
                queryset = queryset.filter(
                    productvariantprice__product_variant_three__variant_title=value
                )
        if title:
            queryset = queryset.filter(title__icontains=title)
        if date:
            year, month, day = date.split("-")
            queryset = queryset.filter(
                created_at__year=year, created_at__month=month, created_at__day=day
            )
        if price_from and price_to:
            queryset = queryset.filter(
                productvariantprice__price__gte=price_from,
                productvariantprice__price__lte=price_to,
            )
        elif price_from:
            queryset = queryset.filter(productvariantprice__price__gte=price_from)

        elif price_to:
            queryset = queryset.filter(productvariantprice__price__lte=price_to)
        return queryset


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "products/edit.html"
    fields = "__all__"
    success_url = reverse_lazy("product:list.product")


def product_edit_view(request, id=None):
    if request.method == "POST":
        product_object = Product.objects.get(id=id)
        form = ProductEditForm(request.POST, instance=product_object)
        if form.is_valid():
            form.save()
            return redirect("product:list.product")
        else:
            return render(
                request,
                "products/edit.html",
                context={"form": form},
            )
    product_object = Product.objects.get(id=id)
    form = ProductEditForm(instance=product_object)
    return render(
        request,
        "products/edit.html",
        context={"form": form},
    )


def product_variant_price_edit_view(request, id=None):
    if request.method == "POST":
        instance = ProductVariantPrice.objects.get(id=id)
        form = ProductVariantPriceEditForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("product:list.product")
        else:
            return render(
                request,
                "products/product_variant_price_edit.html",
                context={"form": form},
            )
    instance = ProductVariantPrice.objects.get(id=id)
    form = ProductVariantPriceEditForm(instance=instance)
    return render(
        request,
        "products/product_variant_price_edit.html",
        context={"form": form},
    )


@csrf_exempt
def product_create_view(request):
    print(request.method)
    if request.method == "POST":
        print(request.POST)
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"})
        else:
            errors_dict = form.errors
            err = ""
            for key, value in errors_dict.items():
                err = err + key + ": "
                err = err + value[0] + "\n"
                err = err + " "

            return JsonResponse({"status": "failed", "error": err})
    context = {}
    variants = Variant.objects.filter(active=True).values("id", "title")
    context["product"] = True
    context["variants"] = list(variants.all())
    return render(request, "products/create.html", context=context)
