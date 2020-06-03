from django.shortcuts import render, get_object_or_404
from scraper.models import Product

# Create your views here.
def product_list(request):
    return render(request, 'product_list/product_list.html', {'products': Product.objects.all()})

def product_info(request, product_id):
    return render(request, 'product_list/product_info.html', {'opinions': Product.objects.get(product_id=product_id).opinions_list})