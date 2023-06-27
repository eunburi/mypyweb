from django.db import models
from django.urls import reverse


# Category 모델 만들기
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    meta_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, db_index=True,
                            unique=True, allow_unicode=True) # 경로 / allow_unicode=True : 한글 허용

    class Meta:
        ordering = ['name'] # 카테고리 이름으로 정렬
        verbose_name = 'category' #관리자페이지에서 카테고리로 나옴
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):   # product 페이지 경로
        return reverse('shop:product_in_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True,
                            unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True) # 상세설명
    meta_description = models.TextField(blank=True) #검색할때
    price= models.DecimalField(max_digits=10, decimal_places=2) #integer로 해도됨 # 소수2째자리까지
    stock = models.PositiveIntegerField()  #재고수량
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)


    created = models.DateTimeField(auto_now_add=True)   # 상품등록일, 필수
    updated = models.DateTimeField(auto_now=True)       # 수정일 , 선택

    class Meta:
        ordering = ['-created', '-updated'] # 내림차순
        index_together = [['id', 'slug']]  # index 기준으로혼합사용

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])