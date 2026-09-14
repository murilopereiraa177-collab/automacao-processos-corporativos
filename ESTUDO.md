# Guia de Estudo

Conceitos que aparecem neste projeto, organizados por tema. Cada item é algo que foi realmente usado no código — serve como checklist do que revisar.

## Python — base

- Funções, parâmetros e retorno de valores
- Tratamento de exceções (`try` / `except`)
- Módulos e importação entre arquivos (`import`)
- Manipulação de dicionários e listas
- Expressões regulares (`re`) — usadas para limpar o CNPJ (remover pontos e traços)
- Ambientes virtuais (`venv`) — isolar as bibliotecas do projeto das do sistema
- Gerenciador de pacotes `pip` e o arquivo `requirements.txt`

## Pandas

- Leitura de planilhas Excel (`pd.read_excel`)
- Validação de dados linha a linha (campos obrigatórios, formato de CNPJ/email)
- Filtragem de linhas válidas/inválidas

## OpenPyXL

- Geração de arquivos Excel formatados (relatório final)
- Escrita de múltiplas abas/seções num mesmo arquivo (resumo, aprovados, pendentes)

## Requests e APIs

- Requisições HTTP GET (`requests.get`)
- Códigos de status HTTP (200 = sucesso, 404 = não encontrado, 429 = limite excedido)
- Timeout em requisições
- Tratamento de erros de rede (`RequestException`)
- Consumo da BrasilAPI (API pública de CNPJ)

## SQL e MySQL

- Criação de banco de dados (`CREATE DATABASE IF NOT EXISTS`)
- Criação de tabelas (`CREATE TABLE`)
- Restrição `UNIQUE` para evitar duplicidade
- Inserção de dados (`INSERT INTO`)
- Conexão Python-MySQL com a biblioteca `mysql-connector-python`
- Verificação de existência de registro antes de inserir

## Selenium (RPA)

- Automação de navegador (`webdriver.Chrome`)
- Localização de elementos na página (`By.ID`)
- Preenchimento de formulários web via automação
- Verificação de resultado da automação (checar se a mensagem de sucesso apareceu)

## Flask

- Criação de uma aplicação web simples
- Rotas e formulários HTML
- Armazenamento temporário de dados em memória (sem banco)

## Logging

- Configuração de logger (`logging`)
- Níveis de log: informação (`info`), aviso (`warning`), erro (`error`)
- Geração de arquivos de log diários

## Variáveis de ambiente

- Arquivo `.env` para guardar credenciais fora do código
- Biblioteca `python-dotenv` para carregar essas variáveis
- Diferença entre `.env` (real, nunca commitado) e `.env.example` (modelo, sem dados sensíveis)

## Organização de projeto

- Separação em pastas por responsabilidade (`api`, `database`, `automation`, `processing`, `utils`)
- Arquivo `main.py` como ponto de entrada, orquestrando o fluxo completo
- Arquivo `.gitignore` (o que não deve ir para o repositório)