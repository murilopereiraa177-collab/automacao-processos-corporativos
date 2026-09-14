# Automação de Processos Corporativos com Python

Projeto de portfólio que simula, de ponta a ponta, um processo real de empresa: o recebimento de solicitações de cadastro de fornecedores por planilha, sua validação, enriquecimento via API pública, persistência em banco de dados e cadastro automatizado num sistema interno via RPA (Selenium) — tudo registrado em log, com tratamento de erros em cada etapa.

## Problema

Empresas frequentemente recebem solicitações de cadastro de fornecedores por planilha, e o processo de conferir, validar e cadastrar cada um manualmente é repetitivo, sujeito a erro humano e demorado.

## Objetivo

Automatizar esse fluxo com Python: ler a planilha de entrada, validar os dados, consultar a situação cadastral de cada CNPJ numa fonte pública, salvar o resultado num banco de dados, cadastrar os fornecedores aprovados num sistema interno (simulado) via automação de navegador, e gerar um relatório final — sem intervenção manual.

## Solução

O projeto simula esse processo de ponta a ponta usando **apenas dados fictícios** — nenhum dado real de cliente, credencial real ou sistema interno de verdade é usado.

O fluxo (orquestrado por `main.py`):

1. Lê a planilha `data/input/solicitacoes.xlsx`
2. Valida cada linha (CNPJ, email e campos obrigatórios)
3. Para cada linha válida, consulta o CNPJ na [BrasilAPI](https://brasilapi.com.br/) (dados públicos da Receita Federal)
4. Salva o resultado no banco MySQL (aprovado ou pendente, sem duplicar registros já existentes)
5. Se aprovado, cadastra o fornecedor automaticamente num sistema interno simulado (Flask + Selenium)
6. Gera um relatório final em Excel com o resumo, os aprovados e os pendentes/inválidos (com o motivo de cada erro)

Todas as etapas são registradas em log (`logs/`), com nível de severidade apropriado (informação, aviso ou erro), e falhas em um registro individual não interrompem o processamento dos demais.

## Tecnologias

| Tecnologia | Papel no projeto |
|---|---|
| Python | Linguagem principal |
| Pandas | Leitura e validação da planilha de entrada |
| OpenPyXL | Geração do relatório Excel formatado |
| Requests | Consulta à API pública de CNPJ |
| Selenium | Automação do cadastro no sistema interno (RPA) |
| Flask | Sistema interno simulado, usado como alvo da automação |
| MySQL | Persistência dos dados dos fornecedores |
| python-dotenv | Configuração de credenciais fora do código-fonte |
| logging (biblioteca padrão) | Registro de eventos, avisos e erros |

## Arquitetura e fluxo

Planilha (Excel)
│
▼
Validação (Pandas)
│
▼
Consulta API (BrasilAPI) ──► CNPJ não encontrado/API indisponível ──► status "pendente"
│
▼ (CNPJ encontrado)
Salvar no MySQL (status "aprovado")
│
▼
Cadastro automático (Selenium + Flask)
│
▼
Relatório final (Excel)

## Estrutura de pastas

ProjetoRPA/
├── data/
│ ├── input/ # Planilha de entrada (dados fictícios)
│ └── output/ # Relatório final gerado
├── src/
│ ├── api/ # Consulta à API de CNPJ
│ ├── database/ # Conexão e operações com o MySQL
│ ├── automation/ # Script de automação com Selenium
│ ├── processing/ # Validação da planilha e geração do relatório
│ └── utils/ # Configuração do sistema de logs
├── webapp_demo/ # Sistema interno simulado (Flask), alvo do Selenium
├── tests/
├── logs/ # Logs diários gerados em tempo de execução
├── sql/
├── .env.example # Modelo das variáveis de ambiente necessárias
├── .gitignore
├── requirements.txt
├── main.py # Ponto de entrada — executa o fluxo completo
└── README.md

## Como instalar e configurar

1. Clone o repositório e entre na pasta:
git clone <url-do-repositorio>
cd ProjetoRPA

2. Crie e ative um ambiente virtual:
python -m venv venv
venv\Scripts\activate

3. Instale as dependências:
pip install -r requirements.txt


4. Copie o arquivo de exemplo de variáveis de ambiente e preencha com suas credenciais do MySQL:
copy .env.example .env


5. Tenha um servidor MySQL rodando localmente (o projeto cria o banco e a tabela automaticamente na primeira execução).

## Como executar

O projeto precisa de dois processos rodando ao mesmo tempo, em terminais separados:

**Terminal 1 — sistema interno simulado:**
python -m webapp_demo.app


**Terminal 2 — fluxo principal:**

python -m main

Ao final, o relatório é gerado em `data/output/relatorio_final.xlsx`, e o log da execução fica disponível em `logs/AAAA-MM-DD.log`.

## Testes

O projeto foi validado manualmente durante o desenvolvimento, testando cada módulo isoladamente (API, banco de dados, Selenium) e depois o fluxo completo via `main.py`, incluindo cenários de erro provocados de propósito (senha de banco incorreta, API indisponível) para confirmar que o tratamento de exceções e o log funcionam corretamente. Testes automatizados (pytest) ainda não foram implementados — ver "Possíveis melhorias futuras".

## Limitações conhecidas

- O projeto usa a BrasilAPI (gratuita) para consulta de CNPJ, que possui limite de requisições (rate limit); em uso intenso, pode retornar erro 429 temporariamente. O sistema trata esse cenário marcando o registro como "pendente" em vez de falhar.
- Os dados de entrada são fictícios, então a maioria dos CNPJs de teste não corresponde a registros reais — isso é intencional, para não usar nenhum dado real.
- O sistema interno "alvo" da automação (Flask) é uma simulação simplificada, criada especificamente para este projeto demonstrar o RPA de forma segura, sem depender de um sistema corporativo real.

## Possíveis melhorias futuras

- Adicionar testes automatizados (pytest) cobrindo as funções de validação, consulta à API e persistência no banco
- Adicionar retries com espera progressiva (backoff) nas chamadas à API
- Rodar o processo em um agendador (ex: tarefa agendada do Windows) para execução periódica automática