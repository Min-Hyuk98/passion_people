import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

path = "C:/Users/Jang/passion_people_jupyter/"
df = pd.read_csv(path+"unused_40_df_bottom.csv",engine="python")
# print(df.head())

tag_list = []
for i, tag in enumerate((df['tags'])):
    tag = tag[1:-1]
    tag = tag.replace("'","")
    tag = tag.replace(",","")
    tag_list.append(tag.split())
# print(tag_list)


df['num'] = 1
# print(df.head())
df0 = df[df['cluster']==1]
# print(df0.head())
# df0['tags'] = df0['tags'].unique()


basket = df0.groupby(['date', 'tags'])['num'].sum().unstack().reset_index().fillna(0).set_index('date')
# basket.to_csv(path+"rules2.csv",encoding="cp949",index = False)

def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = basket.applymap(encode_units)
print(basket_sets.head())
# print("AAa")
frequent_itemsets = apriori(basket_sets, min_support=0.02, use_colnames=True)
print("aa")
frequent_itemsets.to_csv(path+"unused_42_association_bottom.csv",encoding="cp949",index = False)
# print("vv")
# print(frequent_itemsets.head())
# # rules1 = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
# # rules1.head()
# # rules1.columns
# # rules1 = rules1[ (rules1['lift'] > 1) & (rules1['confidence'] >= 0.7) ]


# df = df[df['최종 구분']=='판디엔']
# df.columns
# #df[df['상품명']=='MAC MAKE PREP-PRIME LIP']['구매수량'].sum()
# #df['브랜드 카테고리(대)'].unique()
# df = df[df['브랜드 카테고리(대)']=='Cosmetic & Perfume 2']

# df['여권번호'] = df['여권번호'].apply(lambda x: "%d" % x) #문자화
# df['당일고객'] = df['매출일자']+"_"+df['여권번호']
# df['당일고객'][0:5]

# #strip() - 문자열 양쪽 끝을 자른다. 제거할 문자를 인자로 전달 (디폴트는 공백)
# df['상품명'] = df['상품명'].str.strip()
# test = "  안녕 하세요   "
# test.strip()


# df['당일고객'] = df['당일고객'].astype('str')
# #df = df[~df['그룹번호'].str.contains('C')]

# basket = (df.groupby(['여권번호', '상품명'])['구매수량']
#           .sum().unstack().reset_index().fillna(0)
#           .set_index('여권번호'))
# #basket.head()

# def encode_units(x):
#     if x <= 0:
#         return 0
#     if x >= 1:
#         return 1

# basket_sets = basket.applymap(encode_units)
# basket_sets.head()
# #basket_sets.drop('POSTAGE', inplace=True, axis=1)
# basket_sets.columns

# frequent_itemsets = apriori(basket_sets, min_support=0.01, use_colnames=True)
# frequent_itemsets.head()
# rules1 = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
# rules1.head()
# rules1.columns
# rules1 = rules1[ (rules1['lift'] > 1) & (rules1['confidence'] >= 0.7) ]
# import re

# rules1.to_csv(path+"rules2.csv",encoding="cp949",index = False)
# rules1 = pd.read_csv(path+"rules1.csv",engine = "python")
# rules1['antecedents'] = rules1['antecedents'].apply(lambda x: re.sub("frozenset","",x))
# rules1['consequents'] = rules1['consequents'].apply(lambda x: re.sub("frozenset","",x))
# rules1.to_csv(path+"rules1.csv",encoding="cp949",index = False)
# basket['BOY LONDON'].sum()
# basket['WHOO'].sum()



# b1 = basket_sets[(basket_sets['MAC MAKE Lipstick-Chili'] == 1) | (basket_sets['MAC MAKE PREP-PRIME LIP'] == 1)]
# b2.to_csv(path+"b2.csv",encoding="cp949")
# b2 = pd.read_csv(path+"b2.csv",engine="python")
# b2['매출일자'] = b2['당일고객'].apply(lambda x: x.split("_")[0])
# b2['여권번호'] = b2['당일고객'].apply(lambda x: x.split("_")[1])

# b3 = b2[b2['여권번호'] == b2['여권번호'][77]]
# b3.head()
# #T.FORD BEAUTY
# df.columns
# df1 = df[['브랜드명(소)','순매출금액_원화','구매수량']]
# df1[df1['브랜드명(소)'] == "T.FORD BEAUTY"].groupby('브랜드명(소)').sum()
