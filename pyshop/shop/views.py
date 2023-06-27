from django.shortcuts import render, get_object_or_404
#(404처리)

from shop.models import Category, Product  # 임포트


def index(request):
    return render(request, 'shop/index.html')

def product_in_category(request, category_slug=None):
    current_category = None # 초기화
    categories = Category.objects.all()
    products= Product.objects.filter(available_display=True)

    if category_slug:
        #현재카테고리 1개 가져옴
        current_category = get_object_or_404(Category, slug=category_slug) # 카테고리하나가져옴
        products = products.filter(category=current_category)

    context = {'current_category': current_category,
               'categories': categories,
               'products': products
               }

    return render(request, 'shop/list.html', context)

#상세페이지
def product_detail(request,id,product_slug=None):
    product = get_object_or_404(Product,id=id,slug=product_slug)
    context = {'product':product}
    return render(request, 'shop/detail.html', context)