# Filtro de Comentários Bemol Online - API  
  
API para validação de comentários de produtos na Bemol Online. Aplica as seguintes regras:  
* comentários repetidos;  
* palavras de baixo calão;  
* palavras repetidas três vezes ou mais;  
* sequência de quatro dígitos ou mais;  
* sequência de cinco consoantes ou mais;  
* presença de alguns caracteres especiais incomuns;  
  
## Modelo de requisição  
As requisições são feitas pelo ?SAP? e devem possuir a seguinte estrutura semelhante ao exemplo: 
  
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