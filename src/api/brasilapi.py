import requests
import re

from src.utils.logger import configurar_logger

logger = configurar_logger("brasilapi")


def limpar_cnpj(cnpj: str) -> str:
    """Remove pontos, barra e traço, deixando só os números."""
    return re.sub(r"\D", "", cnpj)


def consultar_cnpj(cnpj: str) -> dict:
    """
    Consulta a BrasilAPI para um CNPJ e retorna os dados encontrados.
    Se a API estiver fora do ar ou o CNPJ não for encontrado, retorna
    um dicionário indicando erro (sem quebrar o programa).
    """
    cnpj_numeros = limpar_cnpj(cnpj)
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_numeros}"

    try:
        resposta = requests.get(url, timeout=10)

        if resposta.status_code == 200:
            dados = resposta.json()
            logger.info(f"CNPJ {cnpj_numeros} encontrado: {dados.get('razao_social')}")
            return {
                "sucesso": True,
                "razao_social": dados.get("razao_social"),
                "situacao_cadastral": dados.get("descricao_situacao_cadastral"),
                "endereco": f"{dados.get('logradouro', '')}, {dados.get('municipio', '')} - {dados.get('uf', '')}",
                "cnae": dados.get("cnae_fiscal_descricao"),
            }
        else:
            logger.warning(f"CNPJ {cnpj_numeros} não encontrado (status {resposta.status_code})")
            return {
                "sucesso": False,
                "motivo": f"CNPJ não encontrado (status {resposta.status_code})",
            }

    except requests.exceptions.RequestException as erro:
        # API fora do ar, sem internet, timeout, etc. — não é erro fatal,
        # o registro deve ficar como "pendente" e o processo continua.
        logger.error(f"Erro ao consultar API para o CNPJ {cnpj_numeros}: {erro}")
        return {
            "sucesso": False,
            "motivo": f"Erro ao consultar API: {erro}",
        }


# Teste rápido
if __name__ == "__main__":
    # CNPJ real só para testar se a consulta funciona (Banco do Brasil)
    resultado = consultar_cnpj("00.000.000/0001-91")
    print(resultado)