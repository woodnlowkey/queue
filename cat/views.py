from django.shortcuts import render
from eunjeon import Mecab
import torch
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
from keras.preprocessing.sequence import pad_sequences
from .apps import CatConfig

models = {'정치': CatConfig.pol_model, 'IT': CatConfig.it_model, '세계': CatConfig.wor_model, '스포츠': CatConfig.spo_model}
mecab = Mecab()
#학습된 bert 모델 불러오기
device = torch.device('cpu')
bert_model = torch.load('.\\static\\bert_model\\epoch_5_evalAcc_94.pth', map_location=device)
model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=4)
model.load_state_dict(bert_model)
model.eval()


# Create your views here.
# 기능 : 카테고라이저 메인 페이지(cat/classifier.html) 호출
# 최종 업데이트: 2021/01/06
# 최종 작업자: 조강희 (bert 모델 추가)
# input
# request: 서버 요청
# output
# return render(request, 'cat/classifier.html', context) : request가 있을 경우 context를 활용해 cat/classifier.html 파일 호출
# context : {'top_result_list': list, 'bottom_result_list': list, 'bert_top' : list, 'bert_bot': list}
# top_result_list, bottom_result_list : [[(),[]], ..., : 결과가 있는 만큼의 리스트]
# bert_top, bert_bot : [str, [float, float, float, float]]
def index(request):
    kw = request.GET.get('kw', '')
    # 키워드가 있을 경우  인자로 w2v함수 호출
    if len(kw) >= 300:
        top_result_list = w2v(kw[:len(kw)//2])
        bottom_result_list = w2v(kw[len(kw)//2:])
        bert_top = bfsc(kw[:len(kw)//2])
        bert_bot = bfsc(kw[len(kw)//2:])
    else:
        top_result_list, bottom_result_list, bert_top, bert_bot = [], [], [], []
    context = {'top_result_list': top_result_list, 'bottom_result_list': bottom_result_list, 'bert_top' : bert_top, 'bert_bot':bert_bot}
    return render(request, 'cat/classifier.html', context)

# 기능 : 키워드에 대한 카테고라이징 결과 리턴
# 최종 업데이트: 2021/01/04
# 최종 작업자: 최우진
# input
# kw : str
# output
# result_list : [(str : 카테고리, str : 카테고리 점수), list([str, str, str, str, str] : 유사키워드 목록)]
def w2v(kw):
    # 입력된 키워드의 명사 추출
    word_list = mecab.nouns(kw)
    # 각 카테고리의 점수
    score = {'정치':0, 'IT':0, '세계':0, '스포츠':0}
    # 유사 키워드 목록
    similar_words = {'정치':[], 'IT':[], '세계':[], '스포츠':[]}
    # 추출된 명사들 word2vec 모델에서 유사한 키워드를 찾음
    for word in word_list:
        # 4가지 카테고리의 모델에서
        for category in models.keys():
            try:
                # 유사한 키워드의 갯수(최대10개)를 카테고리의 점수에 추가
                # 유사한 키워드를 목록에 추가
                similar = models[category].most_similar(word)
                if similar:
                    score[category] += len(similar)
                    similar_words[category] += [word for word, _ in similar]
            # 유사한 키워드가 없는 경우(사전에 등록되지 않은 단어) 유사 키워드 목록 초기화
            except KeyError:
                similar = []
    # 가장 높은 점수를 획득한 카테고리(들)의 점수(백분율=최대90%)와 카테고리명을 반환
    score_key_value = [(k, f'{v/len(word_list)*9:.2f}%') for k, v in score.items() if v != 0 and max(score.values()) == v]
    score_key_words = [similar_words[i] for i, _ in score_key_value]
    # 결과가 없을 경우 빈 리스트를 반환하여 템플릿에서 입력 없음을 안내하도록
    if score_key_words:
        key_words = top_key_words(score_key_words)
        result_list = zip(score_key_value, key_words)
    else:
        result_list = []
    return result_list

# 기능 : 가장 많이 언급된 유사 키워드를 찾는 함수
# 최종 업데이트: 2021/01/04
# 최종 작업자: 최우진
# input
# score_key_words : [str, str, str, str, str, ..., str]
# output
# sort_ words : [str, str, str, str, str]
def top_key_words(score_key_words):
    sort_words = []
    # 해당하는 카테고리의 키워드 리스트로
    for i in score_key_words:
        # 임시 리스트(키워드의 등장 횟수를 카운트 하기 위함)
        temp_word = i
        temp_word_count = []
        # 키워드와 등장 횟수를 카운트하여 임시 리스트에 저장
        for k in set(temp_word):
            temp_word_count.append((k, temp_word.count(k)))
        # 내림차순으로 정렬하여 상위 5개의 키워드만 반환
        temp_list = sorted(temp_word_count, key=lambda x:x[1], reverse=True)
        sort_words.append([l[0] for l in temp_list[:5]])
    return sort_words

# 기능 : 텍스트의 토큰화
# 최종 업데이트: 2021/01/04
# 최종 작업자: 조강희
# input
# kw : [str]
# output
# ids : [int,int,int,int,int,int, ..., int]
def tokenization(kw):
    tokenizer = BertTokenizer.from_pretrained(
        'bert-base-multilingual-cased',
        do_lower_case=False
    )
    tokenized = list(map(tokenizer.tokenize,kw))
    ids = list(map(tokenizer.convert_tokens_to_ids, tokenized))
    return ids

# 기능 : 토큰화 된 id의 길이를 128로 맞추기 위해 패딩 넣기
# 최종 업데이트: 2021/01/04
# 최종 작업자: 조강희
# input
# ids : tokenization 함수에서 return된 ids
# output
# ids : tokenization 함수에서 return된 ids에 패딩을 입힌 값
def padding(ids):
    ids = pad_sequences(ids, maxlen=128, dtype='long', truncating='post', padding='post')
    return ids

# 기능 : 어텐션 마스크 생성
# 최종 업데이트: 2021/01/04
# 최종 작업자: 조강희
# input
# ids : tokenization 함수에서 return된 ids
# output
# masks : tokenization 함수에서 return된 ids를 바탕으로 생성된 어텐션 마스크
def make_attention_mask(ids):
    masks = []
    for id in ids:
        mask = [1 if i > 0 else 0 for i in id]
        masks.append(mask)
    return masks

# 기능 : tokenization, padding, make_attention_mask 함수를 종합적으로 실행하는 함수
# 최종 업데이트: 2021/01/04
# 최종 작업자: 조강희
# input
# kw : str
# output
# predict_ids : 텍스트를 토큰화 후 id값 부여, 패딩 삽입
# predict_masks : predict_ids 를 바탕으로 만들어진 어텐션 마스크
def convert_predict_data(kw):
    kw = [kw]
    predict_ids = tokenization(kw)
    predict_ids = padding(predict_ids)
    predict_masks = make_attention_mask(predict_ids)
    predict_ids = torch.tensor(predict_ids)
    predict_masks = torch.tensor(predict_masks)
    return predict_ids, predict_masks

# 기능 : BERT 모델을 사용한 문서 예측
# 최종 업데이트: 2021/01/04
# 최종 작업자: 조강희
# input
# kw : str
# output
# [predictied_cat, logits] : [str, [float, float, float, float]]
def bfsc(kw):
    inputs, masks = convert_predict_data(kw)
    with torch.no_grad():
        outputs = model(inputs, token_type_ids=None, attention_mask=masks)
    logits = outputs[0]
    predictied_cat = ''
    if np.argmax(logits) == 0:
        predictied_cat = "정치"
    elif np.argmax(logits) == 1:
        predictied_cat = "세계"
    elif np.argmax(logits) == 2:
        predictied_cat = "스포츠"
    elif np.argmax(logits) == 3:
        predictied_cat = "IT"   
    logits = list(map(lambda x:round(x, 5),logits.tolist()[0]))
    return [predictied_cat, logits]