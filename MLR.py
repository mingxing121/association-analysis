import statsmodels.formula.api as smf
import statsmodels.api as sm
import numpy as np
import pandas as pd

path = 'D:\����ʵ��2\ͳ�Ʒ���\�ع����/A����������ָ��.csv'
data = pd.read_csv(path)

data = pd.DataFrame(data,columns=data.columns)


mod = smf.ols(formula='hgamma12~halpha12+hbeta12',data=data)
res = mod.fit()
print(res.summary())

X=np.c_[data['hbeta12'].values,data['halpha12'].values]
print(X)
y=data['hgamma12'].values
# �ع�ϵ���ļ���
X=sm.add_constant(X)
beta_hat=np.dot(np.dot(np.linalg.inv(np.dot(X.T,X)),X.T),y)
print('�ع�ϵ����',np.round(beta_hat,4))

# R^2,�����ϵ��
y_hat=np.dot(X,beta_hat)
y_mean=np.mean(y)
sst=np.sum((y-y_mean)**2) #��ƽ���ͣ���y��ȥy��ֵ����ƽ����
sse=np.sum((y-y_hat)**2)#�в�ƽ���ͣ�yֵ��ȥy�ع�ֵ֮���ƽ����
R_squared=1-sse/sst #R��
R= np.sqrt(R_squared)
print('�����ϵ���ǣ�',R)


