# coding: utf-8
import re

from flask import Flask, request
from flask_restful import Resource, Api

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
api = Api(app)

app.config['JSON_AS_ASCII'] = False


class Filtros(Resource):

    def post(self):
        N_REPETICAO_PALAVRAS = 3

        arq = request.get_json(force=True)
        df = pd.DataFrame(arq)

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
            with open('data/bad_words.txt', 'r', encoding='utf8') as file:
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
            regex = re.compile(r'\d{4,}|[^aeiou .,áàãâéêíóôú0-9]{5,}|[#$&*/\\:;<=>@§£¢¬©\[\]{|}~^]')
            if regex.search(atrib[i]) is not None:
                ind_reprovados[i] = 1

        return {'id': list(df.index), 'STATUS': ind_reprovados.tolist()}


api.add_resource(Filtros, '/filtro')

if __name__ == '__main__':
    app.run(debug=True)
