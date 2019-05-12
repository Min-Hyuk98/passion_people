#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[12]:


import requests
from bs4 import BeautifulSoup
from translate import Translator



#gender=f 또는 gender=m 를 url에 포함시킨다 --> 각각 따로 분석하려함
#sellitem = 1을 url에 포함시킨다 --> 현재 판매중인 옷을 입은 사진만 보여줌
#.area=001,002,004,007,003를 url에 포함시킨다 --> 서울지역만 보여줌
#.&age=10,20,30를 ,url에 포함시킨다 --> 10~30대까지만 보여줌

#마지막 페이지 번호는 .totalPagingNum에서 가져온다
firstPage = 1
lastPage = 1

# 로그인 세션 만들어서, 이 안에서 코드 실행
with requests.session() as s:

    musinsa_data_list = []

    url = "https://store.musinsa.com/app/api/login/make_login"
    data = {
        "referer" : "https://www.musinsa.com/index.php",
        "id" : "wkdalsgur85",
        "pw" : "cnj140535",
    }
    response = s.post(url, data=data)
    response.raise_for_status
#     print(response.text)

    r = requests.get('https://www.musinsa.com/index.php?m=street&_y=2018&gender=f&area=001,002,004,007,003')
    html = r.text
#     print(html)
    soup = BeautifulSoup(html, 'html.parser')

# 마지막 페이지 번호를 구함
    lastPage = soup.find('span',class_='totalPagingNum').get_text()
#     print(lastPage) #lastPage는 str타입

# 바깥 페이지에서 모든 페이지에 하나하나 접근함(성별, 지역, 연령, 시기는 밑의 url에 포함)
    for i in range(firstPage, int(lastPage) + 1):
        r = requests.get('https://www.musinsa.com/index.php?m=street&_y=2018&gender=f&area=001,002,004,007,003&p='+ str(i))
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

# 각 아이템에 접근함
        tmp_list = soup.findAll('a', class_='creplyCnt')
        for item in tmp_list:
            if 'href' in item.attrs:
                uid = item.attrs['href']
                uid = uid[-17:-8]
#                 print(uid)



# 각 아이템의 링크에 들어감
                new_url = "https://www.musinsa.com/index.php?m=street&" + uid
                r = s.post(new_url, data=data)
#                 print(r.text)
                beautifulSoup = BeautifulSoup(r.text, 'html.parser')
#                 print(beautifulSoup)

# 한 아이템 내에서 아우터, 상의, 하의의 사진과 정보만 골라서 분류함
                photo1 = []
                photo2 = []
                photo3 = []
                num = 1
                for tag in beautifulSoup.select('ul > li > div.itemImg > a > img'):
#                     print(num)
                    if num == 1:
                        raw_explanations = beautifulSoup.select('ul > li:nth-of-type(1) > div.itemImg > div > ul > li > a > span')
                        if any("아우터" in s or "상의" in s or '하의' in s for s in raw_explanations):
                            raw_photos = beautifulSoup.select('ul > li:nth-of-type(1) > div.itemImg > a > img')
                            photo1.append(raw_photos[0].get("src"))
                            for i in raw_explanations:
                                photo1.append(i.get_text())
#                         print(photo1)

                    elif num == 2:
                        raw_explanations = beautifulSoup.select('ul > li:nth-of-type(2) > div.itemImg > div > ul > li > a > span')
                        if any("아우터" in s or "상의" in s or '하의' in s for s in raw_explanations):
                            raw_photos = beautifulSoup.select('ul > li:nth-of-type(2) > div.itemImg > a > img')
                            photo2.append(raw_photos[0].get("src"))
                            for i in raw_explanations:
                                photo2.append(i.get_text())
#                         print(photo2)
                    elif num == 3:
                        raw_explanations = beautifulSoup.select('ul > li:nth-of-type(3) > div.itemImg > div > ul > li > a > span')
                        if any("아우터" in s or "상의" in s or '하의' in s for s in raw_explanations):
                            raw_photos = beautifulSoup.select('ul > li:nth-of-type(3) > div.itemImg > a > img')
                            photo2.append(raw_photos[0].get("src"))
                            for i in raw_explanations:
                                photo3.append(i.get_text())
#                         print(photo3)
                    else:
                        print("error!!!!.... the number of items is more than 3")
                    num += 1
# 아이템중 아우터, 상의, 하의중 아무것도 없는 것은  제외함
                if not photo1 and not photo2 and not photo3:
                    continue
# # 구글번역기로 영어로 번역
# # https://pypi.org/project/translate/
# # googletrans issue.......... 다른 라이브러리로 대체
#                 translator= Translator(to_lang="en", from_lang = "ko")
# #                 translation = translator.translate("펜")
# #                 print(translation)
# # photo1 영어로 번역
#                 num = 0
#                 tmp = []
#                 for name in photo1:
#                     if num > 0:
#                         tmp.append(translator.translate(name))
#                     else:
#                         num = 1
#                 del photo1[1:]
#                 photo1.extend(tmp)
# #                 print(photo1)
# #photo2 영어로 번역
#                 num = 0
#                 tmp = []
#                 for name in photo2:
#                     if num > 0:
#                         tmp.append(translator.translate(name))
#                     else:
#                         num = 1
#                 del photo2[1:]
#                 photo2.extend(tmp)
# #                 print(photo2)
# # photo3 영어로 번역
#                 num = 0
#                 tmp = []
#                 for name in photo3:
#                     if num > 0:
#                         tmp.append(translator.translate(name))
#                     else:
#                         num = 1
#                 del photo3[1:]
#                 photo3.extend(tmp)
# #                 print(photo3)


# 아이템의 정보
                raw_list = beautifulSoup.select('table > tbody > tr > td > span')

                info_list = []
                for i in raw_list:
                    info_list.append(i.get_text())
# 예외 없애줌
                if '2018 F/W 헤라 서울패션위크' in info_list:
                    info_list.pop(3)
                elif '2018 서머 뮤직 페스티벌' in info_list:
                    info_list.pop(3)
                elif "2018 MUSINSA MD'S PICK" in info_list:
                    info_list.pop(3)
                elif '2018 F/W 하우스 오브 반스' in info_list:
                    info_list.pop(3)
                elif '2018 신학기 스타일 가이드 북' in info_list:
                    info_list.pop(3)
                elif '2018 스웨트 페스티벌' in info_list:
                    info_list.pop(3)
                elif '2018 S/S 일본 트렌드 리포트' in info_list:
                    info_list.pop(3)
                elif '2018 F/W 버쉬카 도쿄 리포트' in info_list:
                    info_list.pop(3)
                elif '2018 아우터 페스티벌' in info_list:
                    info_list.pop(3)
                elif '2019 S/S 헤라 서울패션위크' in info_list:
                    info_list.pop(3)
                elif '2018 서머 뮤직 페스티벌' in info_list:
                    info_list.pop(3)

#                 print(info_list)

                date = info_list[1]
                style = info_list[5]
                views_like = info_list[6]

# 각각 따로 모은 데이터들을 합치기
                if photo1:
                    photo1.append(date)
                    photo1.append(style)
                    photo1.append(views_like)
                    musinsa_data_list.append(photo1)
#                     print(photo1)
                if photo2:
                    photo2.append(date)
                    photo2.append(style)
                    photo2.append(views_like)
                    musinsa_data_list.append(photo2)
#                     print(photo2)
                if photo3:
                    photo3.append(date)
                    photo3.append(style)
                    photo3.append(views_like)
                    musinsa_data_list.append(photo3)
#                     print(photo3)


#                 print(musinsa_data_list)
#                 print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#         print('a')
# print(musinsa_data_list)


# In[ ]:





# ## 전처리 과정

# In[2]:


#수집한 데이터를 데이터프레임에 저장
data=pd.DataFrame(musinsa_data_list)


# In[ ]:


#수집한 데이터들의 컬럼을 임의로 수정
data.columns=['url','tag1','tag2','tag3','tag4','tag5','tag6','tag7']


# In[ ]:


data_set=data.copy()


# In[ ]:


del data['url']


# In[ ]:


#null값을 0으로 수정
data.loc[data['tag7'].isnull(),'tag7']=0


# In[ ]:


#특수기호나 숫자를 제거
import re
def cleanText(readData):
    text = re.sub('[-/.~]','',readData)
    return text
def cleannum(readData):
    text = re.sub('[0-9]','',readData)
    return text

data['tag4']=data['tag4'].apply(lambda x: cleanText(x))
data['tag4']=data['tag4'].apply(lambda x: cleannum(x))

data['tag5']=data['tag5'].apply(lambda x: cleanText(x))
data['tag5']=data['tag5'].apply(lambda x: cleannum(x))

data['tag6']=data['tag6'].apply(lambda x: cleanText(x))
data['tag6']=data['tag6'].apply(lambda x: cleannum(x))


# In[ ]:


data_copy=data.copy()


# In[ ]:


# 각 컬럼에 있던 태그들을 하나의 컬럼에 리스트로 저장
data_copy['total_tags']=data_copy.apply(lambda x: [x['tag1'],x['tag2'],x['tag3'],x['tag4'],x['tag5'],x['tag6'],x['tag7']],axis=1)


# In[ ]:


# 저장한 컬럼들에 있는 특수기호, 숫자, none 값 제거
def cleanText(readData):
    text = re.sub('[-/.~]','',readData)
    return text
def cleannum(readData):
    text = re.sub('[0-9]','',readData)
    return text
def cleannone(readData):
    text = re.sub('None','',readData)
    return text

data_copy['total_tags']=data_copy['total_tags'].apply(lambda x: cleanText(str(x)))
data_copy['total_tags']=data_copy['total_tags'].apply(lambda x: cleannum(str(x)))
data_copy['total_tags']=data_copy['total_tags'].apply(lambda x: cleannone(str(x)))


# In[1]:


# 콤마(,)를 기준으로 나눠서 각 리스트의 요소들을 컬럼에 저장
data_copy['pre_tag1']=data_copy['total_tags'].apply(lambda x: x.split(',')[0])
data_copy['pre_tag2']=data_copy['total_tags'].apply(lambda x: x.split(',')[1])
data_copy['pre_tag3']=data_copy['total_tags'].apply(lambda x: x.split(',')[2])
data_copy['pre_tag4']=data_copy['total_tags'].apply(lambda x: x.split(',')[3])
data_copy['pre_tag5']=data_copy['total_tags'].apply(lambda x: x.split(',')[4])
data_copy['pre_tag6']=data_copy['total_tags'].apply(lambda x: x.split(',')[5])


# In[ ]:


# 컬럼에 저장된 각 요소들 중에 특수 기호(') 제거
data_copy['pre_tag1']=data_copy['pre_tag1'].apply(lambda x: re.sub("'",'',x))
data_copy['pre_tag1']=data_copy['pre_tag1'].apply(lambda x: x[1:])
data_copy['pre_tag2']=data_copy['pre_tag2'].apply(lambda x: re.sub("'",'',x))
data_copy['pre_tag3']=data_copy['pre_tag3'].apply(lambda x: re.sub("'",'',x))
data_copy['pre_tag4']=data_copy['pre_tag4'].apply(lambda x: re.sub("'",'',x))
data_copy['pre_tag5']=data_copy['pre_tag5'].apply(lambda x: re.sub("'",'',x))
data_copy['pre_tag6']=data_copy['pre_tag6'].apply(lambda x: re.sub("'",'',x))


# In[ ]:


# 컬럼에 저장된 각 요소들 중에 특수 기호(공백) 제거
data_copy['pre_tag2']=data_copy['pre_tag2'].apply(lambda x: re.sub(" ",'',x))
data_copy['pre_tag3']=data_copy['pre_tag3'].apply(lambda x: re.sub(" ",'',x))
data_copy['pre_tag4']=data_copy['pre_tag4'].apply(lambda x: re.sub(" ",'',x))
data_copy['pre_tag5']=data_copy['pre_tag5'].apply(lambda x: re.sub(" ",'',x))
data_copy['pre_tag6']=data_copy['pre_tag6'].apply(lambda x: re.sub(" ",'',x))


# In[ ]:


data_copy['pre_tag3']=data_copy['pre_tag3'].apply(lambda x: str(x))


# In[30]:


data_copy.head()


# ## 한글을 영어로 변환하는 과정

# In[34]:


get_ipython().system('pip install googletrans')
from googletrans import Translator
translator = Translator()


# ## tag1~6에 있는 한글 태그를 영어로 변환

# In[ ]:


data_copy['en_pre_tag1'] = data_copy['pre_tag1'].apply(translator.translate, src='ko', dest='en').apply(getattr, args=('text',))


# In[ ]:


translator = Translator()
data_copy['en_pre_tag2'] = data_copy['pre_tag2'].apply(translator.translate, src='ko', dest='en').apply(getattr, args=('text',))


# In[ ]:


translator = Translator()
data_copy['en_pre_tag3'] = data_copy['pre_tag3'].apply(translator.translate, src='ko', dest='en').apply(getattr, args=('text',))


# In[ ]:


translator = Translator()
data_copy['en_pre_tag4'] = data_copy['pre_tag4'].apply(translator.translate, src='ko', dest='en').apply(getattr, args=('text',))


# In[ ]:


translator = Translator()
data_copy['en_pre_tag5'] = data_copy['pre_tag5'].apply(translator.translate, src='ko', dest='en').apply(getattr, args=('text',))


# In[ ]:


translator = Translator()
data_copy['en_pre_tag6'] = data_copy['pre_tag6'].apply(translator.translate, src='ko', dest='en').apply(getattr, args=('text',))


# In[42]:


data_copy.head()


# ## 단어의 최소 단위로 쪼개기

# In[43]:


data_copy['en_pre_tag1'].value_counts()


# In[ ]:


# Crotty로 되어 있는 영어를 올바르게 변환
data_copy.loc[data_copy['en_pre_tag1']=='Crotty','en_pre_tag1']='Crop Top'


# ## 2개 이상의 단어로 구성된 구를 각각의 단어로 쪼개서 저장

# In[ ]:


import numpy as np
data_copy['en_pre_tag1_1']= np.nan
data_copy['en_pre_tag1_2']= np.nan


# In[ ]:


data_copy['en_pre_tag1_1']=data_copy.loc[data_copy['en_pre_tag1'].isin(['Track pants','Bra Top','Denim shorts','Crop Top']),'en_pre_tag1'].apply(lambda x: x.split(' ')[0])
data_copy['en_pre_tag1_2']=data_copy.loc[data_copy['en_pre_tag1'].isin(['Track pants','Bra Top','Denim shorts','Crop Top']),'en_pre_tag1'].apply(lambda x: x.split(' ')[1])


# In[60]:


data_copy['en_pre_tag5'].value_counts()


# In[ ]:


import numpy as np
data_copy['en_pre_tag5_1']= np.nan
data_copy['en_pre_tag5_2']= np.nan
data_copy['en_pre_tag5_3']= np.nan


# In[ ]:


data_copy['en_pre_tag5_1']=data_copy.loc[data_copy['en_pre_tag5'].isin(['Sexy Feminine','Unique kitsch']),'en_pre_tag5'].apply(lambda x: x.split(' ')[0])
data_copy['en_pre_tag5_2']=data_copy.loc[data_copy['en_pre_tag5'].isin(['Sexy Feminine','Unique kitsch']),'en_pre_tag5'].apply(lambda x: x.split(' ')[1])


# In[ ]:


data_copy['en_pre_tag5_1']=data_copy.loc[data_copy['en_pre_tag5'].isin(['Street hip hop']),'en_pre_tag5'].apply(lambda x: x.split(' ')[0])
data_copy['en_pre_tag5_2']=data_copy.loc[data_copy['en_pre_tag5'].isin(['Street hip hop']),'en_pre_tag5'].apply(lambda x: x.split(' ')[1:])


# In[ ]:


data_copy['en_pre_tag5_3']=data_copy.loc[data_copy['en_pre_tag5'].isin(['Street hip hop']),'en_pre_tag5'].apply(lambda x: str(' '.join(x.split(' ')[1:])))


# In[84]:


data_copy['en_pre_tag6'].value_counts()


# In[ ]:


import numpy as np
data_copy['en_pre_tag6_1']= np.nan
data_copy['en_pre_tag6_2']= np.nan


# In[ ]:


data_copy['en_pre_tag6_1']=data_copy.loc[data_copy['en_pre_tag6'].isin(['Street hip hop']),'en_pre_tag6'].apply(lambda x: x.split(' ')[0])
data_copy['en_pre_tag6_2']=data_copy.loc[data_copy['en_pre_tag6'].isin(['Street hip hop']),'en_pre_tag6'].apply(lambda x: str(' '.join(x.split(' ')[1:])))


# ## 전처리를 완료한 태그들을 final_set에 저장

# In[ ]:


final_set=data_copy[['en_pre_tag1_1','en_pre_tag1_2','en_pre_tag2','en_pre_tag3','en_pre_tag4','en_pre_tag5_1','en_pre_tag5_2','en_pre_tag5_3','en_pre_tag6_1','en_pre_tag6_2']]


# In[90]:


# 태그들을 하나의 컬럼에 리스트로 저장
final_set['example_final']=final_set.apply(lambda x: [x['en_pre_tag1_1'],x['en_pre_tag1_2'],x['en_pre_tag2'],x['en_pre_tag3'],x['en_pre_tag4'],x['en_pre_tag5_1'],x['en_pre_tag5_2'],x['en_pre_tag5_3'],x['en_pre_tag6_1'],x['en_pre_tag6_2']],axis=1)


# ## 전처리 및 변환을 마친 word들을 수치화 시키는 과정 : Word2 vec 모델

# In[92]:


get_ipython().system('pip install gensim')


# In[107]:


# nan값을 제거
final_set['example_end']=final_set['example_final'].apply(lambda y: pd.Series(y).dropna().values.tolist())


# In[4]:


import pandas as pd
final_set=pd.read_csv('final_set.csv')
final_set.head()


# In[29]:


all_training_words = [word for example in final_set["example_end"] for word in example]
training_sentence_lengths = [len(example) for example in final_set["example_end"]]
TRAINING_VOCAB = sorted(list(set(all_training_words)))
print("%s words total, with a vocabulary size of %s" % (len(all_training_words), len(TRAINING_VOCAB)))
print("Max sentence length is %s" % max(training_sentence_lengths))


# ## 구글의 미리 학습된 word2vec 모델 사용

# In[30]:


import gensim

# Load Google's pre-trained Word2Vec model.
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)


# In[31]:


# 수치화된 모든 벡터 저장
word_vectors=model.wv
# 모든 벡터에 대한 단어 저장
vocabs = word_vectors.vocab.keys()
# 우리의 태그들에 대한 벡터
word_vectors_list= [word_vectors[v] for v in vocabs]


# ## 학습된 모델 사용시 벡터의 평균 점수 사용
# - 밑의 함수에 대한 요약 해석
#
# : 한 사진마다 태그가 없으면 벡터화할 단어가 없으므로 0 값
#
# : 단어가 있다면 태그 하나당 수치화(벡터화)의 수준을 300개로 할당
#
# -- ex) crop에 대한 점수(벡터)- 300개
# - 결론: 각 단어마다 300개의 수치화된 점수로 구성된다.

# In[35]:


import numpy as np
def get_average_word2vec(tokens_list, vector, generate_missing=False, k=300):
    if len(tokens_list)<1:
        return np.zeros(k)
    if generate_missing:
        vectorized = [vector[word] if word in vector else np.random.rand(k) for word in tokens_list]
    else:
        vectorized = [vector[word] if word in vector else np.zeros(k) for word in tokens_list]
    length = len(vectorized)
    summed = np.sum(vectorized, axis=0)
    averaged = np.divide(summed, length)
    return averaged

def get_word2vec_embeddings(vectors, clean_comments, generate_missing=False):
    embeddings = final_set['example_end'].apply(lambda x: get_average_word2vec(x, vectors,
                                                                                generate_missing=generate_missing))
    return list(embeddings)


# In[36]:


training_embeddings = get_word2vec_embeddings(model, final_set, generate_missing=True)


# ## 벡터로 변환한 데이터들을 pca를 통하여 데이터를 축소시키고 kmeans를 통하여 3개의 군집으로 클러스터링 완료

# In[37]:


from sklearn.decomposition import PCA
from matplotlib import pyplot
# 태그들을 벡터화 시킨 값을 x에 저장
# 2개의 성분으로 벡터들을 축소
pca = PCA(n_components=2)
X = pca.fit_transform(training_embeddings)
# kmeans 클러스터링을 이용해 군집
from sklearn import cluster
from sklearn import metrics
NUM_CLUSTERS=3
kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS)
kmeans.fit(X)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_


# In[38]:


final=pd.DataFrame(X)
final.columns=['x1','x2']
final['label']=labels
final.head()


# In[8]:


final['url']= data_set['url']


# In[39]:


final['tags']=final_set['example_end']
final.head()


# In[46]:


final.to_csv('fianl_project_dataset.csv',index=False,mode='w')


# In[ ]:
