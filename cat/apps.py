from django.apps import AppConfig
from gensim.models import KeyedVectors

class CatConfig(AppConfig):
    name = 'cat'
    # 카테고리별로 학습된 word2vec 모델 불러오기
    pol_model = KeyedVectors.load_word2vec_format('.\static\w2v_model\pol_w2v')
    it_model = KeyedVectors.load_word2vec_format('.\static\w2v_model\it_w2v')
    wor_model = KeyedVectors.load_word2vec_format('.\static\w2v_model\wor_w2v')
    spo_model = KeyedVectors.load_word2vec_format('.\static\w2v_model\spo_w2v')
    
    
