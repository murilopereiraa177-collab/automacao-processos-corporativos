from src.processing.validador import carregar_e_validar
from src.api.brasilapi import consultar_cnpj
from src.database.criar_banco import criar_banco_e_tabela
from src.database.salvar_fornecedor import salvar_fornecedor
from src.automation.preencher_formulario import preencher_formulario
from src.processing.relatorio import gerar_relatorio
from src.utils.logger import configurar_logger

logger = configurar_logger("main")

CAMINHO_ENTRADA = "data/input/solicitacoes.xlsx"
CAMINHO_SAIDA = "data/output/relatorio_final.xlsx"


def processar_fornecedor(linha):
    """
    Processa uma linha válida da planilha: consulta o CNPJ na API,
    define o status, salva no banco e cadastra no sistema via Selenium
    (se aprovado). Retorna o status final ('aprovado' ou 'pendente').
    """
    cnpj = linha["cnpj"]
    resultado_api = consultar_cnpj(cnpj)

    if resultado_api["sucesso"]:
        status = "aprovado"
        dados = {
            "cnpj": cnpj,
            "razao_social": resultado_api.get("razao_social"),
            "situacao_cadastral": resultado_api.get("situacao_cadastral"),
            "endereco": resultado_api.get("endereco"),
            "cnae": resultado_api.get("cnae"),
            "email": linha["email"],
            "status": status,
        }
    else:
        status = "pendente"
        dados = {
            "cnpj": cnpj,
            "razao_social": linha.get("nome"),
            "situacao_cadastral": None,
            "endereco": None,
            "cnae": None,
            "email": linha["email"],
            "status": status,
        }

    salvar_fornecedor(dados)

    if status == "aprovado":
        fornecedor_selenium = {
            "nome": dados["razao_social"] or linha["nome"],
            "cnpj": cnpj,
            "categoria": linha.get("categoria", "Fornecedor Geral"),
        }
        confirmado = preencher_formulario(fornecedor_selenium)
        if not confirmado:
            logger.warning(f"Cadastro via Selenium não confirmado para o CNPJ {cnpj}")

    return status


def main():
    logger.info("Iniciando processamento de solicitações")

    criar_banco_e_tabela()

    validos, invalidos = carregar_e_validar(CAMINHO_ENTRADA)

    for _, linha in validos.iterrows():
        try:
            processar_fornecedor(linha)
        except Exception as erro:
            logger.error(f"Erro ao processar o fornecedor {linha.get('cnpj', '?')}: {erro}")

    gerar_relatorio(validos, invalidos, CAMINHO_SAIDA)

    logger.info("Processamento concluído")


if __name__ == "__main__":
    main()