quando existe repetição da mesma palavra na letra, está considerando somente a primeira ocorrencia portanto está repentindo, por exemplo ne letra.txt tem: 
Deus aonde está 
Aonde está 
Aonde está 
Aonde está 

e o outut.json ficou assim:
  {
    "text": "Deus aonde está",
    "timestamp": 11.56,
    "confidence": 100.0
  },
  {
    "text": "Aonde está",
    "timestamp": 12.96,
    "confidence": 100.0
  },
  {
    "text": "Aonde está",
    "timestamp": 12.96,
    "confidence": 100.0
  },
  {
    "text": "Aonde está",
    "timestamp": 12.96,
    "confidence": 100.0
  },

o resultado esperado é:

  {
    "text": "Deus aonde está",
    "timestamp": 11.56,
    "confidence": 100.0
  },
  {
    "text": "Aonde está",
    "timestamp": 14.01,
    "confidence": 100.0
  },
  {
    "text": "Aonde está",
    "timestamp": 16.96,
    "confidence": 100.0
  },
  {
    "text": "Aonde está",
    "timestamp": 20.46,
    "confidence": 100.0
  },

portanto me de 3 estrategias para o script identificar ocorrencias repetidas e considerar isso na leitura do audio
