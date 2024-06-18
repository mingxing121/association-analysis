import statsmodels.formula.api as smf
import statsmodels.api as sm
import numpy as np
import pandas as pd

path = 'D:\综述实验2\统计分析\回归分析/A类高信噪比线指数.csv'
data = pd.read_csv(path)

data = pd.DataFrame(data,columns=data.columns)


mod = smf.ols(formula='hgamma12~halpha12+hbeta12',data=data)
res = mod.fit()
print(res.summary())

X=np.c_[data['hbeta12'].values,data['halpha12'].values]
print(X)
y=data['hgamma12'].values
# 回归系数的计算
X=sm.add_constant(X)
beta_hat=np.dot(np.dot(np.linalg.inv(np.dot(X.T,X)),X.T),y)
print('回归系数：',np.round(beta_hat,4))

# R^2,复相关系数
y_hat=np.dot(X,beta_hat)
y_mean=np.mean(y)
sst=np.sum((y-y_mean)**2) #总平方和：即y减去y均值后差的平方和
sse=np.sum((y-y_hat)**2)#残差平方和：y值减去y回归值之差的平方和
R_squared=1-sse/sst #R方
R= np.sqrt(R_squared)
print('复相关系数是：',R)


