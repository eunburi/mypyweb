import os

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# 카테고리 모델
class Category(models.Model):
    # unique=True - 중복불허
    name = models.CharField(max_length=50, unique=True)
    #url주소 - 문자
    slug = models.SlugField(max_length=50, unique=True,
        allow_unicode =True)

    def __str__(self):
        return self.name

# 카테고리 url 주소
    def get_absolute_url(self):
        # return f'/blog/category/{self.slug}'
        # reverse() - redirect 유사 : app-name으로 경로 이동
        return reverse('blog:category_page', args=[self.slug])

# 관리자페이지에서 적용 - verbose_name_plural
    class Meta:
        ordering = ['name'] # 이름순 정렬
        verbose_name = 'category'
        verbose_name_plural = 'categories'


#포스트모델
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  #제목
    content = models.TextField()              #내용
    pub_date = models.DateTimeField()         #발행일
    modify_date = models.DateTimeField(null=True, blank=True) #입력 폼이 비어도 됨
    photo = models.ImageField(upload_to='blog/images/%Y/%m/%d/',
                    null=True, blank=True)  #null 허용, 이미지 파일을 첨부하지 않을수 있음
    file = models.FileField(upload_to='blog/files/%Y/%m/%d/',
                    null=True, blank=True )
    # models.Set_Null카테고리가 삭제되어도 카테고리가 없는 포스트는 유지
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    #파일의 이름 출력
    def get_file_name(self):
        return os.path.basename(self.file.name)

    # 파일의 확장가 구분
    def get_file_ext(self):
        # seoul.csv -> [seoul, csv]
        return self.get_file_name().split('.')[-1]
