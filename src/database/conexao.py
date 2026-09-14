import os
import mysql.connector
from dotenv import load_dotenv

from src.utils.logger import configurar_logger

load_dotenv()

logger = configurar_logger("conexao")


def obter_conexao(usar_banco=True):
    """
    Cria e retorna uma conexão com o MySQL.
    Se usar_banco=False, conecta sem especificar um banco (usado para criar o banco pela primeira vez).
    """
    config = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    if usar_banco:
        config["database"] = os.getenv("DB_NAME")

    try:
        conexao = mysql.connector.connect(**config)
        logger.info("Conexão com o MySQL estabelecida com sucesso")
        return conexao
    except mysql.connector.Error as erro:
        logger.error(f"Erro ao conectar ao MySQL: {erro}")
        raise