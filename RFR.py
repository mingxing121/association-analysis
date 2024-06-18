# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import warnings
warnings.filterwarnings("ignore")




# 读取数据
df = pd.read_csv('D:\综述实验2\统计分析\回归分析/A类高信噪比线指数.csv')


# 计算所有元素线指数的相关系数
pd.set_option('display.max_columns', None)    #可以显示所有的列
print(df.iloc[:,:].corr())



from sklearn.preprocessing import StandardScaler

sc_X = StandardScaler()
s_data = sc_X.fit_transform(df)
df = pd.DataFrame(s_data,columns=df.columns)

# 线性回归模型类
X = df.loc[:, ['halpha12','hbeta12','hdelta12']].values
y = df.loc[:, 'hgamma12'].values.reshape(-1,1)





regressor = RandomForestRegressor(n_estimators=5, random_state=42)
regressor.fit(X,y)

# Predicting a new result
y_pred = regressor.predict(X)





# 读取数据

df = pd.read_csv('D:\综述实验2\统计分析\回归分析/A类高信噪比线指数.csv')

sc_X = StandardScaler()
s_data = sc_X.fit_transform(df)
df = pd.DataFrame(s_data,columns=df.columns)

# 线性回归模型类
X = df.loc[:, ['halpha12','hbeta12','hdelta12']].values
y = df.loc[:, 'hgamma12'].values.reshape(-1,1)

random_forest_model = RandomForestRegressor(n_estimators=5,random_state=42)
random_forest_model.fit(X,y)




# # 变量重要性分析

train_X_column_name=['H\u03b1','H\u03b2','H\u03b4']
random_forest_importance=list(random_forest_model.feature_importances_)
random_forest_feature_importance=[(feature,round(importance,8))
                                  for feature, importance in zip(train_X_column_name,random_forest_importance)]


importance_plot_x_values=list(range(len(random_forest_importance)))
plt.bar(importance_plot_x_values,random_forest_importance)
plt.xticks(importance_plot_x_values,train_X_column_name,size=13)
plt.xlabel('Variable',fontname='Times New Roman',size=13)
plt.ylabel('Importance',fontname='Times New Roman',size=13)
plt.yticks(size=9)
plt.title('Variable Importances',size=13,fontname='Times New Roman')

plt.show()