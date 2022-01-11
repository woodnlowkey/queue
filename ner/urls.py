from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'ner'

urlpatterns = [
    # 주소 뒤에 아무것도 입력하지 않았을 때 접속하는 페이지 = ner/news_list.html
    path('', views.index, name='index'),
    # 뉴스를 클릭했을 때 접속하는 페이지 = ner/news_detail.html
    path('<int:news_id>/', views.detail, name='detail'),
]
