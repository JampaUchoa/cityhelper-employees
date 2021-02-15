Serviço REST para trabalhadores da defesa civil realizar requisições feitas a Prefeitura da Cidade do Recife.

O servico recebe da API principal as solicitações em aberto e retorna uma solicitacão a ser feita pelo Operador, 
a depender da prioridade, que é baseada na distancia e a data em qual foi aberta.

## Executando o projeto 

1. Para testar o projeto é necessario estar utilizando o app [front-end da aplicação](http://localhost:3000)
2. Instalar o [poetry](https://python-poetry.org/) e o Python 3.9.0 (da maneira que preferir)
3. Instalar as dependecias com `poetry install`
7. Rodar o serviço com `poetry run uvicorn main:app --reload --port 7500`