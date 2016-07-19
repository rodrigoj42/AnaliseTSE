#-*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from sys import argv

def csv(f):
    a = []
    b = []
    c = open(f)
    for line in c:
        ls = line.split(';')
        try:
            a.append(float(ls[1]))
            b.append(float(ls[3]))
        except:
            print ls
    return [a,b]

teste = csv(argv[1])

plt.scatter(teste[1], teste[0])
#plt.show()
print "GRAFICO PLOTADO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
plt.savefig(argv[1])
