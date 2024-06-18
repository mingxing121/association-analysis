import pandas as pd
from sklearn.linear_model import BayesianRidge
from sklearn.preprocessing import StandardScaler


# 读取数据
data = pd.read_csv('D:\综述实验2\统计分析\回归分析/A类高信噪比线指数.csv')


df = data.loc[:, ['halpha12', 'hdelta12']]

pd.set_option('display.max_columns', None)    #可以显示所有的列
print(data.iloc[:,:].corr())

# 标准化
sc_X = StandardScaler()
s_data = sc_X.fit_transform(df)
df = pd.DataFrame(s_data,columns=df.columns)

# 线性回归模型类
x = df.loc[:, 'halpha12'].values.reshape(-1, 1)
y = df.loc[:, 'hdelta12'].values.reshape(-1, 1)


# 创建一个贝叶斯线性回归模型
model = BayesianRidge(alpha_1=50, lambda_1=10)

# 训练模型
model.fit(x, y)

# 使用训练好的模型进行预测

y_pred = model.predict(x)
print("Predictions:", y_pred) # 输出预测结果