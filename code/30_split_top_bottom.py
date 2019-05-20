import pandas as pd

path = "C:/Users/Jang/passion_people_jupyter/"
df = pd.read_csv(path+"20_item_temperature.csv",engine="python")
# print(df.head())

tag_list = []
for i, tag in enumerate((df['tags'])):
    tag = tag[1:-1]
    tag = tag.replace("'","")
    tag = tag.replace(",","")
    tag_list.append(tag.split())

t_list = []
for i, tag in enumerate(tag_list):
    if '하의' in tag:
        t_list.append("1")
    else:
        t_list.append("0")
df["i_tag"] = t_list

# print(df)

#  상의, 하의로 데이터프레임 2개로 나누기
df_down = df[df['i_tag']=='1']
df_up = df[df['i_tag']=='0']
# print(df_down)

del df_down['i_tag']
del df_up['i_tag']
df_down.to_csv('32_df_bottom.csv',mode='w',index=False,encoding=' CP949')
df_up.to_csv('31_df_top.csv',mode='w',index=False,encoding=' CP949')
