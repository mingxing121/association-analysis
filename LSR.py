# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import seaborn as sns

# 标准化
from sklearn.preprocessing import StandardScaler

# 读取数据
data = pd.read_csv('D:\综述实验2\统计分析\回归分析/A类高信噪比线指数.csv')

# 计算所有元素线指数的相关系数
pd.set_option('display.max_columns', None)    #可以显示所有的列
print(data.iloc[:,:].corr())

df = data.loc[:, ['halpha12', 'hdelta12']]


# 标准化
sc_X = StandardScaler()
s_data = sc_X.fit_transform(df)
df = pd.DataFrame(s_data,columns=df.columns)


# 线性回归模型类
x = df.loc[:, 'halpha12'].values.reshape(-1, 1)
y = df.loc[:, 'hdelta12'].values.reshape(-1, 1)

# 创建模型
model = LinearRegression()

model.fit(x, y)

y_pred = model.predict(x)
print("Predictions:", y_pred) # 输出预测结果


