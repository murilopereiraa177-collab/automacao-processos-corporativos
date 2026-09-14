# Perguntas de Entrevista

**Projeto:** Automação de Processos Corporativos com Python

Perguntas que podem surgir em uma entrevista técnica sobre este projeto, com respostas baseadas apenas no que foi realmente implementado.

---

## Sumário

1. [Visão geral e arquitetura](#visão-geral-e-arquitetura)
2. [Dados e validação](#dados-e-validação)
3. [API e integração externa](#api-e-integração-externa)
4. [Banco de dados](#banco-de-dados)
5. [Selenium / RPA](#selenium--rpa)
6. [Logs e tratamento de erros](#logs-e-tratamento-de-erros)

---

## Visão geral e arquitetura

**1. Me explica esse projeto em poucas palavras.**

É um projeto de portfólio que automatiza o processo de cadastro de fornecedores: lê uma planilha com solicitações, valida os dados, consulta o CNPJ numa API pública, salva no banco MySQL e cadastra automaticamente num sistema simulado via Selenium, gerando um relatório final em Excel.

**2. Por que você dividiu o projeto em pastas (`src/api`, `src/database`, `src/automation`, etc.)?**

Para separar responsabilidades: cada pasta cuida de uma parte do fluxo (consulta à API, banco de dados, automação web, processamento de planilha). Isso deixa o código mais organizado, fácil de entender e de dar manutenção — se eu precisar mexer só na parte do banco, sei exatamente onde procurar.

**3. Por que usar Flask para simular o sistema interno em vez de usar um sistema real?**

Porque não faz sentido nem seria ético automatizar um sistema real de empresa num projeto de portfólio. O Flask criou uma aplicação web simples, só com um formulário de cadastro, que serve como "alvo" seguro para o Selenium praticar a automação, sem depender de nenhum sistema corporativo de verdade.

## Dados e validação

**4. Como você valida os dados da planilha?**

Uso Pandas para ler a planilha e verificar campos obrigatórios, formato de CNPJ e de email. Linhas com dados inválidos não seguem para as próximas etapas — ficam marcadas como pendentes/inválidas no relatório final, com o motivo do erro.

**5. O que acontece se um CNPJ da planilha não existir na Receita Federal?**

A consulta à BrasilAPI retorna que não encontrou o CNPJ, e o sistema marca aquele registro como "pendente" em vez de travar o processo inteiro — os outros registros continuam sendo processados normalmente.

## API e integração externa

**6. Por que escolheu a BrasilAPI?**

Porque é uma API pública e gratuita que fornece dados reais da Receita Federal sobre CNPJs, sem precisar de nenhuma credencial paga ou dado sigiloso — ideal para um projeto de portfólio.

**7. Como você trata erros de conexão com a API?**

Uso `try/except` com a biblioteca `requests`, capturando erros de timeout ou de conexão. Quando a API falha ou demora demais (defini um timeout de 10 segundos), o registro correspondente é marcado como pendente e o erro é registrado no log — sem derrubar o restante do processamento.

**8. O que é rate limit e como isso afeta seu projeto?**

Rate limit é um limite de quantas requisições uma API aceita em um período de tempo. A BrasilAPI, sendo gratuita, tem esse limite. Se eu ultrapassar, ela retorna um erro 429, que meu sistema trata da mesma forma que outras falhas da API: marcando o registro como pendente, sem quebrar o programa.

## Banco de dados

**9. Por que usar MySQL e não outro banco?**

Foi uma escolha para praticar SQL relacional, que é bastante pedido em vagas de TI/dados. O projeto poderia ser adaptado para outro banco relacional sem muita dificuldade, já que a lógica de conexão fica isolada num módulo separado.

**10. Como você evita duplicar fornecedores no banco?**

A coluna `cnpj` na tabela tem uma restrição `UNIQUE`, e antes de inserir um novo registro o sistema verifica se aquele CNPJ já existe no banco.

**11. Onde ficam as credenciais do banco de dados?**

Nunca no código. Ficam num arquivo `.env`, que não é enviado ao GitHub (está no `.gitignore`). O projeto usa a biblioteca `python-dotenv` para ler essas credenciais em tempo de execução. Existe um `.env.example` no repositório só como modelo, sem dados reais.

## Selenium / RPA

**12. Como funciona a automação com Selenium nesse projeto?**

O script abre o navegador, acessa o formulário do sistema simulado em Flask, preenche os campos (nome, CNPJ, categoria) usando os IDs dos elementos HTML, clica no botão de salvar e confirma se a mensagem de sucesso apareceu na tela.

**13. Por que automatizar um sistema web e não uma área de trabalho, por exemplo?**

Porque automação de sistemas web via navegador é uma das aplicações mais comuns de RPA no mercado, e o Selenium é a ferramenta padrão para isso — fazia sentido praticar esse cenário.

## Logs e tratamento de erros

**14. Por que registrar logs no projeto?**

Para ter rastreabilidade: se algo der errado durante a execução, consigo abrir o arquivo de log do dia e ver exatamente o que aconteceu, em vez de tentar adivinhar. Uso diferentes níveis (informação, aviso, erro) dependendo da gravidade do evento.

**15. O que você faria diferente ou o que falta melhorar?**

Ainda não implementei testes automatizados com pytest — os testes foram feitos manualmente, testando cada módulo separadamente e depois o fluxo completo, incluindo cenários de erro provocados de propósito. Também penso em adicionar retentativas automáticas (retries) nas chamadas à API e talvez rodar o processo em um agendador de tarefas.