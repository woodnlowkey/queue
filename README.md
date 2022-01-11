# queue-2 #
1. ## 개요 ##
	- 뉴스기사 NER 및 어뷰징 기사 판별
	1. ### 수행기간 ###
		- 2021.12.13 ~ 2022.01.12
	2. ### 사용언어 ###
		- Python
	3. ### 목적 ###
		- 광고성 기사의 판별 기능을 구축하여 어뷰징 실태를 확인함으로써 대중매체가 사실을 정직하고 공정하게 전달하는데 기여하고자 함
	4. ### 주요내용 ###
		- Django 활용 웹페이지 구축
		- 버터블록 개체명 인식(NER) API 활용 뉴스 기사 내 키워드 색상 변환 기능 제작
		- Word2Vec, BERT Pre-trained model 활용 어뷰징 뉴스 판별 기능 제작
		- 개발 단계별 산출물 작성
2. ## 계획 ##
	1. ### 과제 범위 확인 ###
		- 구현 기능 설정
		- 필요 라이브러리 탐색 및 스터디
		- 요구사항 목록 작성[데이터 검색 기능, NER 기능, 광고성 기사 판별 기능, 관리자 기능]
		- 요구사항 정의서 작성[요구사항분류 및 번호, 명칭, 유형, 상세설명, 산출물]
		- 업무 분장
	2. ### 기존 과제 연계점 탐색 ###
		- 1차 프로젝트 연계(Naver 뉴스기사 18,656건을 수집하여 중복 기사 정제 결과 11674건)
3. ## 설계 ##
	1. ### 시스템 / 화면 구조 설계 ###
		- Application[DB 내 키워드 검색과 정렬, NER 결과 기사 내 키워드 색상 표현, 뉴스 분류기(광고성 기사 판별)]
		- Server[Django, SQLite(Database), Classifier Model(Word2Vec, BERT)] / NER버터블록의 구성
	2. ### ERD / 테이블 정의 ###
		- 테이블 정의서 작성(ner_newsData[id/INT/NOT NULL/AUTO INCREMENT:PK, subject/VARCHAR(200)/NOT NULL, category/VARCHAR(25)/NOT NULL, create_date/DATETIME/NOT NULL, content/TEXT/NOT NULL, author/VARCHAR(40)/NOT NULL])
	3. ### 개발 표준 / 테스트 시나리오 ###
		- 함수 및 변수명 작성 규칙, 예외처리에 대한 부분, 주석 형식(작성일자, 작성자)
		- 단위 테스트, 통합 테스트 시나리오 작성
4. ## 구현 ##
	- 환경[운영체제:Windows, Requirements:VisualStudioC++데스크톱개발환경설치/3.6.0<=Python<=3.9.0, Django/eunjeon/gensim/tensorflow>=2.0.0/torch/transformers설치]
	1. ### Django Project ###
		- Templates(HTML, Bootstrap(CSS, JavaScript), ORM 사용)
		- Named Entity Recognition(㈜TwoBlockAI에서 제공한 학습용 NER모델 API 활용)
	2. ### Classifier ###
		- Word2Vec:유사 키워드 기반 데이터 분석 모델 구현
		- BERT(BertForSequenceClassification):transfer learning
5. ## 테스트 ##
	- 개발 기능 별 단위 테스트 병행
	- 테스트 시나리오 보완
	- 서버 환경(Linux, MacOS) 및 멀티 브라우저(Chrome, Edge, Firefox)테스트
	- 프로젝트 완료 보고서 작성

_woodnlowkey(woojin choi, vxrs3310@gmail.com)_
=====
- 조원들과 함께하는 작업에서 실무적인 계획, 설계 작업의 필요성을 느낄 수 있었습니다. Django 프레임워크를 공부하고 활용하면서 웹 어플리케이션의 동작 원리를 이해할 수 있었고 가상환경의 개념적인 부분과 작업 환경에서 문제 해결능력을 키울 수 있는 기회가 되었습니다.	
	- 참여:과제 범위 확인, 구현 기능 설정, 요구사항 정의서 작성, 시스템 구조 설계, 문서 작성, 화면 구조 설계, 문서 작성, 테이블 설계 및 ERD, 테이블 정의서 작성, 테스트 시나리오 작성, NER 인덱싱 오류 문제에 대한 문장별 request 설계, Huggingface Transformers 이용 BERTmodel 사용을 위한 서버 환경 설정, 구현 단계별 단위테스트 실행, AWS Lightsail(Linux) 서버(Nginx, Gunicorn) 환경 테스트, Chrome, Edge, Firefox 브라우저 통합 테스트
	- 구현:기존 과제 연계 사용을 위한 1차 프로젝트 데이터 정제, Django framework를 사용하여 웹 UI설계·구현, HTML, Bootstrap4의 CSS·Javascript 이용 템플릿 구현, Django에서 제공하는 객체·관계형 데이터베이스 연결방식(ORM) 이용 SQLite 데이터베이스 구현, 뉴스 리스트 페이지 구현, 최신순·관련순 검색, 정렬, 페이지 기능 구현, 뉴스 본문 NER결과 페이지 구현, 어뷰징 뉴스 판별 Classifire 페이지 구현, 1차 수집·정제 데이터 사용 Gensim Word2Vec 모델 생성, 학습된 모델 이용 유사 키워드 기반 카테고라이저 구현
