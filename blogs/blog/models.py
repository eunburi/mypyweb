from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100) # 제목 - 자릿수가 정해진거
    content = models.TextField() #내용 - 무제한
    pub_date = models.DateTimeField() #발행일 - 날짜시간
    modify_date = models.DateTimeField(null=True, blank=True) #수정일 - db용으로 null 허용 / blank : 입력 폼에 비어도 됨
    # photo = models.ImageField(upload_to='blog/images/%Y/%m/%d/',
    #                           null=True, blank=True) # null허용, 파일을 첨부하지 않을수 있음
    photo = models.ImageField(upload_to='blog/images/%Y/%m/%d/',
                              null=True, blank=True)

    def __str__(self):
        return self.title #관리자 페이지에서 한글로

