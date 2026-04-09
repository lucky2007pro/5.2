from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import ProductForm
from .models import Product


class ProductListView(View):
    def get(self, request):
        products = Product.objects.select_related("category", "owner").filter(is_active=True)
        return render(request, "product_list.html", {"products": products})


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product.objects.select_related("category", "owner"), pk=pk)
        return render(request, "product_detail.html", {"product": product})


class ProductCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProductForm()
        return render(request, "product_form.html", {"form": form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, "Mahsulot qo'shildi.")
            return redirect("my_products")
        return render(request, "product_form.html", {"form": form})


class ProductUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.owner != request.user:
            return HttpResponseForbidden("Siz faqat o'zingizning mahsulotingizni tahrirlaysiz.")

        form = ProductForm(instance=product)
        return render(request, "product_form.html", {"form": form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.owner != request.user:
            return HttpResponseForbidden("Siz faqat o'zingizning mahsulotingizni tahrirlaysiz.")

        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Mahsulot yangilandi.")
            return redirect("product_detail", pk=product.pk)
        return render(request, "product_form.html", {"form": form})


class ProductDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.owner != request.user:
            return HttpResponseForbidden("Siz faqat o'zingizning mahsulotingizni o'chirasiz.")
        return render(request, "product_confirm_delete.html", {"object": product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.owner != request.user:
            return HttpResponseForbidden("Siz faqat o'zingizning mahsulotingizni o'chirasiz.")

        product.delete()
        messages.success(request, "Mahsulot o'chirildi.")
        return redirect("my_products")


class MyProductsView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.select_related("category").filter(owner=request.user)
        return render(request, "my_products.html", {"products": products})
