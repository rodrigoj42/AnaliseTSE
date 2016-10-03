from prettytable import PrettyTable 

t = open('dados_rj.txt').readlines()

candidatos = []
for linha in t[2:-1]:
    candidatos.append(eval(linha[:-3]))
candidatos.append(eval(t[-1][:-4]))

coligacoes = {}
for candidato in candidatos:
    h = candidato['cc'].find('-')
    if h == -1: coligacao = candidato['cc']
    else: coligacao = coligacao = candidato['cc'][h+2:]
    try: coligacoes[coligacao] += int(candidato['v'])
    except: coligacoes[coligacao] = int(candidato['v'])

qe = sum(coligacoes.values())/51.0

eleitos = []

tabela = PrettyTable(['Coligacao', 'N Candidatos', 'Votos', 'Quociente Partidario'])
for coligacao in coligacoes:
    c_da_c = filter(lambda x: coligacao == x['cc'] if x['cc'].find('-') == -1 else coligacao == x['cc'][x['cc'].find('-')+2:], candidatos)
    s = sorted(c_da_c, key=lambda x: int(x['v']))[::-1]
    qp = int(coligacoes[coligacao]/qe)
    tabela.add_row([coligacao, len(s), coligacoes[coligacao], qp])
    coligacoes[coligacao] = {'cadeiras':qp, 'votos':coligacoes[coligacao], 'candidatos':s}
    for eleito in s[:qp]: eleitos.append(eleito)
print tabela
print 'Coeficiente Eleitoral: %s \n' % str(int(qe))

blacklist = []
while len(eleitos) < 51:
    temp = {}
    for coligacao in coligacoes:
        try: 
            if coligacao not in blacklist and coligacoes[coligacao]['votos'] > qe:
                temp[coligacoes[coligacao]['votos']/float(coligacoes[coligacao]['cadeiras']+1)] = coligacao
            else:
                pass
        except: pass
    coligacao = temp[max(temp.keys())]
    eleito = coligacoes[coligacao]['candidatos'][coligacoes[coligacao]['cadeiras']]
    if int(eleito['v']) > int(0.1*qe):
        coligacoes[coligacao]['cadeiras'] += 1
        eleitos.append(eleito)
    else: 
        blacklist.append(coligacao)

target = raw_input('Nome do partido: ')

c_do_p = []
for candidato in candidatos:
    if candidato['cc'][:len(target)] == target:
        c_do_p.append(candidato)
c_do_p = sorted(c_do_p, key=lambda x: int(x['v']))[::-1]

tabela = PrettyTable(['Posicao', 'Nome', 'Votos'])
for candidato in range(len(c_do_p[:25])):
    tabela.add_row([candidato+1, c_do_p[candidato]['nm'], c_do_p[candidato]['v']])
print tabela

raw_input('Aperte ENTER para mostrar os candidatos eleitos')

a = 0
partidos = {}
tabela = PrettyTable(['Posicao', 'Nome', 'Coligacao', 'Votos'])
for eleito in eleitos:
    a += 1
    tabela.add_row([a, eleito['nm'], eleito['cc'], int(eleito['v'])])
    try: partidos[eleito['cc']] += 1
    except: partidos[eleito['cc']] = 1
print tabela 

raw_input('Aperte ENTER para mostrar o numero de candidatos eleitos em cada partido')

tabela = PrettyTable(['Partido', 'N'])
for partido in partidos: tabela.add_row([partido, partidos[partido]])
tabela.sortby = 'N'
print tabela
