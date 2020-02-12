# coding: utf-8
import re

from flask import Flask, request
from flask_restful import Resource, Api

import pandas as pd

app = Flask(__name__)
api = Api(app)

app.config['JSON_AS_ASCII'] = False


class Filtros(Resource):

    def post(self):

        try:
            arq = request.get_json(force=True)
            df = pd.DataFrame(arq, index=arq['PRODUCTREVIEW_ID_SAP'])
        except:
            return "Erro no formato da requisição json", 400

        # procura comentários repetidos
        repets = df.duplicated(subset='COMMENTS')
        ind_reprovados = [1 if repetido else 0 for repetido in repets]

        # extraindo palavrões
        with open('data/bad_words.txt', 'r', encoding='utf8') as file:
            proibidas = file.read().split()

        atrib = []
        for i in range(len(df)):

            # juntando título e comentário
            atrib.append(str(df.NAME.values[i]).lower() + ' ' + str(df.COMMENTS.values[i]).lower())

            # removendo palavras comuns
            palavras_comuns = [' a ', ' o ', ' e ', ' um ', ' uma ', ' ele ', ' ela ', ' com ', ' de ', ' da ', ' do ']
            for palavra in palavras_comuns:
                atrib[i] = atrib[i].replace(palavra, ' ')

            # procurando palavrões
            for palavra in atrib[i].split():
                if palavra in proibidas:
                    ind_reprovados[i] = 1

            # outros padrões indesejados
            regex = re.compile(r'\d{4,}|[^aeiou .,áàãâéêíóôú0-9]{5,}|(..)\1+|[#$&*/\\:;<=>@§£¢¬©\[\]{|}~^]')
            regex_repetidas = re.compile(r'\b(\w{3}).*\1.*\1') # não consegui juntar os dois regexes
            if (regex.search(atrib[i]) is not None) or (regex_repetidas.search(atrib[i]) is not None):
                ind_reprovados[i] = 1

        return {'PRODUCTREVIEW_ID_SAP': df.index.tolist(), 'STATUS': ind_reprovados}, 200


api.add_resource(Filtros, '/filtro')

if __name__ == '__main__':
    app.run(debug=True)
