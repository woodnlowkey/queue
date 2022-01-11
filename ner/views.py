from django.shortcuts import render, get_object_or_404
from .models import NewsData
from django.core.paginator import Paginator
from django.db.models import Q
import requests
import json

# 기능 : NER 메인 페이지(ner/news_list.html) 호출
# 최종 업데이트: 2021/12/30
# 최종 작업자: 최우진
# input
# request : 서버 요청
# page : int
# kw : str
# so : str
# output
# render(request, 'ner/news_list.html', context) : request가 있을 경우 context를 활용해 ner/news_list.html 파일 렌더링
# context : {'news_list' : paginator object, 'page': int, 'kw': str}
def index(request):
    # 페이징
    page = request.GET.get('page', '1')
    # 검색어
    kw = request.GET.get('kw', '')
    # 최신순 정렬
    so = request.GET.get('so', 'recent')
    # 뉴스 목록 조회
    news_list = NewsData.objects.order_by('-create_date')
    # 검색어가 있을 경우
    if kw:
        news_list = news_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(category__icontains=kw)
        ).distinct()
        # 최신순 정렬을 선택한 경우 그대로 출력
        if so == 'recent':
            pass
        # 관련순 정렬을 선택한 경우
        else:
            sort_list = []
            # 뉴스 리스트 전체에서 제목과 본문 중 키워드를 카운트
            for news in news_list:
                sort_list.append((news.subject.count(kw) + news.content.count(kw), news))
            # 키워드를 많이 포함한 순서로 정렬
            news_list = sorted(sort_list, key=lambda x:x[0], reverse=True)
            news_list = [i[1] for i in news_list]
    # 페이징 처리
    paginator = Paginator(news_list, 20)
    page_obj = paginator.get_page(page)
    context = {'news_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'ner/news_list.html', context)

# 기능 : NER 적용 결과 페이지(ner/news_detail.html) 호출
# 최종 업데이트: 2021/12/30
# 최종 작업자: 최우진
# input
# request: 서버 요청
# news_id : int (뉴스의 id값)
# output
# render(request, 'ner/news_list.html', context) : request가 있을 경우 context를 활용해 ner/news_detail.html 파일 렌더링
# context : {'news': str(DB object)}
def detail(request, news_id):
    # 뉴스 내용 출력
    news = get_object_or_404(NewsData, pk=news_id)
    # iframe_colored = apply_ner(news.content)
    iframe = open('.\static\iframe.html', 'w', encoding='utf8')
    # iframe.write('<p style="color: #f8f9fa; line-height: 1.8;">' + f'{iframe_colored}' + '</p>')
    iframe.close()
    context = {'news': news}
    return render(request, 'ner/news_detail.html', context)

# 기능 : 텍스트에 span 태크를 입혀 반환함(색 입히기 위해)
# 최종 업데이트: 2021/12/31
# 최종 작업자: 조강희
# input
# content : str(html 태그 없는 텍스트)
# output
# final : str(html 태그 붙은 텍스트)
def apply_ner(content):
    # 결과물에 따른 색상 딕셔너리
    colors = {'동물':'#6b60aa;','용어': '#3182bd;','문명':'#3182bd;', '사건':'#cc2673;', '인물':'#ffd400', '기관':'#e6550d;', '지역':'#fdae6b;', '날짜':'#31a354;','시간':'#31a354;', '인공물':'#addd8e;', '수량':'#c994c7;', '물질':'#addd8e;'}
    
    # 문장 나누기
    # split = kss.split_sentences(content)
    split = content.split('. ')
    
    # 최종 결과물이 들어갈 변수
    final = ''
    
    # 문장별로 반복문 돌려 결과물에 색상 적용
    for sentence in split:
        # ner 포맷으로 변경
        sentence_dict = {'texts':[sentence]}
        
        # request and responce
        req = requests.post("http://192.168.0.221:3333/ner", json=sentence_dict)
        res = json.loads(req.text)
        
        # 인덱스 순으로 정렬
        res = sorted(res[0],key=lambda x:x[0])
        
        # 텍스트 삽입과 html 태그 계산을 위한 임시 변수
        cnt_temp = 0
        sentence_temp = list(sentence)
        
        # 답변별로 반복문 돌려 정답 찾기
        for result in res:
            tag_start = f'<span style="color:{colors[result[2]]}">' # 색상 적용
            tag_end = '</span>'
            if result[1] == sentence[result[0]:result[0]+len(result[1])]:
                sentence_temp.insert(result[0]+cnt_temp, tag_start)
                cnt_temp+=1
                sentence_temp.insert(result[0]+len(result[1])+cnt_temp, tag_end)
                cnt_temp+=1
            else:
                continue
        final += ''.join(sentence_temp)
        final += '. '
    
    return final