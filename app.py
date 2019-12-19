# coding: utf-8

import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_excel('data/testes_novembro.xlsx')
df = df.loc[:, ['STATUS', 'NAME']]

df.columns = ['NAME', 'COMMENTS']

N_REPETICAO_PALAVRAS = 3
LEN_PALAVRAS_IGNORADAS = 2

atrib = []
ind_reprovados = np.zeros(len(df))
for i in range(len(df)):

    # juntando título e comentário
    atrib.append(str(df.NAME.values[i]).lower() + ' ' + str(df.COMMENTS.values[i]).lower())

    # procura comentários repetidos
    j = 0
    repets = df.duplicated(subset='COMMENTS')
    for repetido in repets:
        if repetido:
            ind_reprovados[j] = 1
        j += 1

    # procurando palavrões
    proibidas = []
    with open('data/bad_words.txt', 'r') as file:
        words = file.read()

        for palavra in words.split():
            proibidas.append(palavra)

    for palavra in atrib[i].split():
        if palavra in proibidas:
            ind_reprovados[i] = 1

    # procurando palavras repetidas
    palavras_comuns = [' a ', ' o ', ' e ', ' um ', ' uma ', ' ele ', ' ela ', ' com ', ' de ', ' da ', ' do ']
    for palavra in palavras_comuns:
        atrib[i] = atrib[i].replace(palavra, ' ')

    try:
        count = CountVectorizer().fit_transform([atrib[i]])
        n = count.toarray().max()
    except ValueError:
        ind_reprovados[i] = 1
    if n >= N_REPETICAO_PALAVRAS:
        ind_reprovados[i] = 1

    # outros padrões indesejados
    regex = re.compile(r'\d{4,}|[^aeiou .,áàãâéêíóôú0-9]{5,}|[#$&*/\\:;<=>@\[\]{|}~^]')
    if regex.search(atrib[i]) is not None:
        ind_reprovados[i] = 1
df['saida_show'] = ind_reprovados

df.to_excel('saida.xlsx')
