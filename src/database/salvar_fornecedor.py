from src.database.conexao import obter_conexao
from src.utils.logger import configurar_logger

logger = configurar_logger("salvar_fornecedor")


def fornecedor_existe(cnpj):
    """Verifica se um CNPJ já está cadastrado no banco."""
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT id FROM fornecedores WHERE cnpj = %s", (cnpj,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado is not None


def salvar_fornecedor(dados):
    """
    Salva um fornecedor no banco, se ainda não existir.
    'dados' deve ser um dicionário com: cnpj, razao_social, situacao_cadastral,
    endereco, cnae, email, status
    """
    if fornecedor_existe(dados["cnpj"]):
        logger.warning(f"CNPJ {dados['cnpj']} já cadastrado, pulando")
        return False

    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO fornecedores
        (cnpj, razao_social, situacao_cadastral, endereco, cnae, email, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        dados["cnpj"],
        dados.get("razao_social"),
        dados.get("situacao_cadastral"),
        dados.get("endereco"),
        dados.get("cnae"),
        dados.get("email"),
        dados.get("status"),
    ))

    conexao.commit()
    cursor.close()
    conexao.close()

    logger.info(f"Fornecedor {dados['cnpj']} salvo com sucesso")
    return True


# Teste rápido
if __name__ == "__main__":
    fornecedor_teste = {
        "cnpj": "00.000.000/0001-91",
        "razao_social": "BANCO DO BRASIL SA",
        "situacao_cadastral": "ATIVA",
        "endereco": "SAUN QUADRA 5 BLOCO B TORRE I, II, III, BRASILIA - DF",
        "cnae": "Bancos múltiplos, com carteira comercial",
        "email": "teste@teste.com",
        "status": "aprovado",
    }

    salvar_fornecedor(fornecedor_teste)