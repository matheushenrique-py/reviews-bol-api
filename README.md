# Filtro de Comentários Bemol Online - API  
  
API para validação de comentários de produtos na Bemol Online. Aplica as seguintes regras:  
* comentários repetidos;  
* palavras de baixo calão;  
* palavras repetidas três vezes ou mais;  
* sequência de quatro dígitos ou mais;  
* sequência de cinco consoantes ou mais;  
* presença de alguns caracteres especiais incomuns;  
  
## Modelo de requisição  
As requisições POST são feitas pelo ?SAP? ao endpoint _/filtros_ e devem possuir a seguinte estrutura semelhante ao exemplo: 
  
```json  
{  
  "PRODUCTREVIEW_ID_SAP": [92653, 27542, "...", 816408],  
  "NAME": ["Título 1", "Título 2", "...", "Título n"],  
  "COMMENTS": ["Comentário 1", "Comentário 2", "...", "Comentário n"]  
}  
```  
  
## Modelo de resposta  
  
```json  
{  
  "PRODUCTREVIEW_ID_SAP": [92653, 27542, "...", 816408],  
  "STATUS": [1, 0, "...", 0]  
}  
```

Onde:
 * STATUS == 0: comentário aprovado;
 * STATUS == 1: comentário reprovado;

# Lista de palavras censuradas
É possível receber a lista de palavras censuradas com o GET ao endpoint_/palavras_. Da mesma maneira, é possível adicionar novas palavras com um POST com a seguinte estrutura:

```json  
{  
  "PALAVRAS": ["palavra 1", "palavra 2", "...", "palavra n"]  
}  
```