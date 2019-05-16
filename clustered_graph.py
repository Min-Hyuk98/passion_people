import csv
from matplotlib import pyplot as plt

x_list = []
y_list = []
f = open('clustering_V2.csv', 'r', encoding='CP949')
rdr = csv.reader(f)
tmp = 0

# 엑셀데이터에서 좌표데이터만 빼서 리스트로 저장
for line in rdr:
    if tmp == 0:
        tmp += 1
        continue
    else:
        for idx, item in enumerate(line):
            if idx == 2:
                x_list.append(item)
            elif idx == 3:
                y_list.append(item)
#             elif idx == 4:
#                 if item != '0':
#                     del x_list[-1]
#                     del y_list[-1]

# print(x_list)
# print(y_list)

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
