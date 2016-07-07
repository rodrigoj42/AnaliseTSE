import matplotlib.pyplot as plt
from system import argv

def csv(f):
    a = []
    b = []
    c = open(f)
    for line in c:
        ls = line.split(';')
        a.append(float(ls[1]))
        b.append(float(ls[3]))
    return [a,b]

teste = csv(argv[0])

plt.scatter(teste[1], teste[0])
plt.show()
plt.savefig(argv[1])
