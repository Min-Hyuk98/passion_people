import csv
from matplotlib import pyplot as plt

x_list = []
y_list = []
text_list = []
f = open('11_word_clustering.csv', 'r', encoding='CP949')
rdr = csv.reader(f)
tmp = 0

# 엑셀데이터에서 좌표데이터만 빼서 리스트로 저장
for line in rdr:
    if tmp == 0:
        tmp += 1
        continue
    else:
        test = 0
        for idx, item in enumerate(line):
            if idx == 2:
                x_list.append(item)
            elif idx == 3:
                y_list.append(item)

# print(x_list)
# print(y_list)
print(text_list)

# str을 float로 변환
for i, item in enumerate(x_list):
    x_list[i] = float(x_list[i])

for i, item in enumerate(y_list):
    y_list[i] = float(y_list[i])


# print(x_list)
# print(y_list)

# 그래프 그리기
plt.figure()
plt.scatter(x_list,y_list)
plt.show()

f.close()
