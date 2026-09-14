import pandas as pd
import re

from src.utils.logger import configurar_logger

logger = configurar_logger("validador")


def cnpj_valido(cnpj: str) -> bool:
    """Verifica se o CNPJ tem o formato correto: 00.000.000/0000-00"""
    if not isinstance(cnpj, str):
        return False
    padrao = r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"
    return bool(re.match(padrao, cnpj))


def email_valido(email: str) -> bool:
    """Verifica se o email tem um formato básico válido."""
    if not isinstance(email, str):
        return False
    padrao = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(padrao, email))


def campos_obrigatorios_preenchidos(linha: pd.Series) -> bool:
    """Verifica se nome, cnpj, email e categoria não estão vazios."""
    campos = ["nome", "cnpj", "email", "categoria"]
    for campo in campos:
        valor = linha.get(campo)
        if pd.isna(valor) or str(valor).strip() == "":
            return False
    return True


def validar_linha(linha: pd.Series) -> tuple[bool, list[str]]:
    """Valida uma linha e retorna (é_valida, lista_de_erros)."""
    erros = []

    if not campos_obrigatorios_preenchidos(linha):
        erros.append("Campo obrigatório vazio")

    if not cnpj_valido(linha.get("cnpj", "")):
        erros.append("CNPJ em formato inválido")

    if not email_valido(linha.get("email", "")):
        erros.append("Email em formato inválido")

    return (len(erros) == 0, erros)


def carregar_e_validar(caminho_planilha: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Lê a planilha e separa em dois DataFrames: válidos e inválidos.
    O DataFrame de inválidos ganha uma coluna extra 'erros' explicando o motivo.
    """
    df = pd.read_excel(caminho_planilha)

    validos = []
    invalidos = []

    for _, linha in df.iterrows():
        ok, erros = validar_linha(linha)
        if ok:
            validos.append(linha)
        else:
            linha_com_erro = linha.copy()
            linha_com_erro["erros"] = "; ".join(erros)
            invalidos.append(linha_com_erro)
            logger.warning(f"Registro inválido (CNPJ {linha.get('cnpj', '?')}): {'; '.join(erros)}")

    df_validos = pd.DataFrame(validos)
    df_invalidos = pd.DataFrame(invalidos)

    logger.info(f"Validação concluída: {len(df_validos)} válidos, {len(df_invalidos)} inválidos")

    return df_validos, df_invalidos


# Teste rápido: só roda se você executar este arquivo diretamente
if __name__ == "__main__":
    validos, invalidos = carregar_e_validar("data/input/solicitacoes.xlsx")

    print(f"Registros válidos: {len(validos)}")
    print(f"Registros com erro: {len(invalidos)}")
    print("\n--- Válidos ---")
    print(validos[["nome", "cnpj", "email"]])
    print("\n--- Inválidos ---")
    print(invalidos[["nome", "cnpj", "email", "erros"]])