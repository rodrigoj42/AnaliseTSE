#-*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from sys import argv

# Abrindo CSV
def csv(f):
    a = []
    b = []
    c = open(f)
    for line in c:
        ls = line.split(';')
        try:
            #candidato = ls[0]
            a.append(float(ls[1]))
            b.append(float(ls[3]))
        except:
            print ls
    return [a,b]

teste = csv(argv[1])

# Scatterplotando 
x, y = teste[1], teste[0]
plt.scatter(x, y)
#plt.title("Analise")
plt.ylabel("% de votos do candidato na secao")
plt.ylim(0)
plt.xlabel("% do valor do indicador na secao") 
plt.xlim(0)

fit = np.polyfit(x,y,1)
fit_fn = np.poly1d(fit)
plt.plot(x,fit_fn(x), '--k', linewidth=3)


print argv[1]
print "GRAFICO PLOTADO" 
plt.show()
plt.savefig(argv[1]+'.png')
