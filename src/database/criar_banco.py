import os
from dotenv import load_dotenv

from src.database.conexao import obter_conexao
from src.utils.logger import configurar_logger

load_dotenv()

logger = configurar_logger("criar_banco")


def criar_banco_e_tabela():
    # Conecta sem banco específico, só para poder criar o banco
    conexao = obter_conexao(usar_banco=False)
    cursor = conexao.cursor()

    nome_banco = os.getenv("DB_NAME")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nome_banco}")
    logger.info(f"Banco '{nome_banco}' verificado/criado com sucesso")

    cursor.close()
    conexao.close()

    # Agora conecta já usando o banco criado, para criar a tabela
    conexao = obter_conexao(usar_banco=True)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cnpj VARCHAR(18) UNIQUE NOT NULL,
            razao_social VARCHAR(255),
            situacao_cadastral VARCHAR(50),
            endereco VARCHAR(255),
            cnae VARCHAR(255),
            email VARCHAR(255),
            status VARCHAR(20),
            data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    logger.info("Tabela 'fornecedores' verificada/criada com sucesso")

    cursor.close()
    conexao.close()


if __name__ == "__main__":
    criar_banco_e_tabela()