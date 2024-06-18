# -*- coding: UTF-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

df = pd.read_csv('D:\综述实验2\散点图\BPT/snrgi20.csv')
# print(df)

data=df.loc[:,['combined_hbeta_ew', 'combined_oiii_5008_ew', 'combined_halpha_ew', 'combined_nii_6585_ew']]



x=[]
y=[]
i=1
for row in data.values:
    cociente1 = row[3] / row[2]  # NII/Hα
    x.append(np.log10(cociente1))

    cociente2 = row[1] / row[0]  # OIII/Hβ
    y.append(np.log10(cociente2))

#

fig, ax = plt.subplots(facecolor='white',figsize=(4.5, 2.9))
ax.scatter(x,y,marker='o',s=3,color='paleturquoise')
Nsize = 8
ax.set_xlabel(r'log([NII]/H$\alpha$)',fontsize=Nsize)

# ax.set_ylabel(r'log([OIII] $\lambda$5007/H$\beta$)',fontsize=Nsize)
ax.set_ylabel(r'log([OIII]/H$\beta$)',fontsize=Nsize)
#
# ## Kewley+01------------------------------------------
X = np.linspace(-1.5,0.3)
Y = (0.61/(X - 0.47  )) + 1.19
## Kauffmann+03 ---------------------------------------
Xk = np.linspace(-1.5,0)

Yk=(0.61/(Xk -0.05) + 1.3)

## CF10------------------------------------
Xm=np.linspace(-0.185,1)
Ym=1.01*Xm+0.48

ax.plot(X,   Y, '-' , color='blue', lw=1, label='Kewley+01', alpha = 0.4) # Kewley+06

ax.plot(Xk, Yk, '--', color='red', lw=1, label='Kauffmann+03', alpha = 0.4) # Kauffmann+03

ax.plot(Xm,Ym,'--',color='green',lw=1,label='CF10', alpha = 0.4)  #CF10

ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))   #设置x轴次刻度
ax.yaxis.set_minor_locator(plt.MultipleLocator(0.1))   #设置y轴次刻度
ax.tick_params(axis="both", which="minor", direction="out",width=1, length=3,labelsize=7)

plt.tick_params(axis='both', which='major', direction='in',width=1, length=5,labelsize=7)

plt.figtext(0.3, 0.43, f'SF', size=7)
plt.figtext(0.61, 0.22, f'Composite', size=7)
plt.figtext(0.78, 0.37, f'LINER', size=7)
plt.figtext(0.37, 0.77, f'Seyfert II', size=7)

plt.ylim(-2, 1.5)
plt.xlim(-1.25, 0.5)

plt.show()
