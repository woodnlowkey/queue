"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 관리자 페이지에 접속하는 url
    path('admin/', admin.site.urls),
    # 주소 뒤에 아무것도 입력하지 않았을 때 접속하는 페이지 = ner/news_list.html
    path('', include('ner.urls')),
    # 카테고라이저 페이지에 접속하는 url
    path('cat', include('cat.urls')),
    # 팀 소개 페이지에 접속하는 url
    path('team/', include('team.urls')),
]
