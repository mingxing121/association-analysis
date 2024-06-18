import pandas as pd
from sklearn.linear_model import BayesianRidge
from sklearn.preprocessing import StandardScaler


# ��ȡ����
data = pd.read_csv('D:\����ʵ��2\ͳ�Ʒ���\�ع����/A����������ָ��.csv')


df = data.loc[:, ['halpha12', 'hdelta12']]

pd.set_option('display.max_columns', None)    #������ʾ���е���
print(data.iloc[:,:].corr())

# ��׼��
sc_X = StandardScaler()
s_data = sc_X.fit_transform(df)
df = pd.DataFrame(s_data,columns=df.columns)

# ���Իع�ģ����
x = df.loc[:, 'halpha12'].values.reshape(-1, 1)
y = df.loc[:, 'hdelta12'].values.reshape(-1, 1)


# ����һ����Ҷ˹���Իع�ģ��
model = BayesianRidge(alpha_1=50, lambda_1=10)

# ѵ��ģ��
model.fit(x, y)

# ʹ��ѵ���õ�ģ�ͽ���Ԥ��

y_pred = model.predict(x)
print("Predictions:", y_pred) # ���Ԥ����