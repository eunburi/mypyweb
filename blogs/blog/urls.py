
from django.urls import path
from . import views # . - 같은곳이라는 뜻 뷰랑 url이랑 같은 폴더안에 있으니까

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:post_id>/', views.detail, name='detail'), #상세페이지
    path('post/create/', views.post_create, name='post_create'),

]



