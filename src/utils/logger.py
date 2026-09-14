import logging
import os
from datetime import datetime

def configurar_logger(nome_modulo):
    """
    Cria e retorna um logger configurado para gravar mensagens
    tanto no arquivo de log quanto no terminal.
    'nome_modulo' aparece nas mensagens para saber de onde veio o log
    (ex: 'brasilapi', 'selenium', 'banco').
    """
    # Garante que a pasta logs/ existe
    os.makedirs("logs", exist_ok=True)

    # Nome do arquivo de log com a data de hoje (ex: logs/2026-09-14.log)
    nome_arquivo = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

    logger = logging.getLogger(nome_modulo)
    logger.setLevel(logging.INFO)

    # Evita duplicar mensagens se o logger já tiver sido configurado antes
    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler que grava no arquivo
        handler_arquivo = logging.FileHandler(nome_arquivo, encoding="utf-8")
        handler_arquivo.setFormatter(formato)

        # Handler que mostra no terminal também
        handler_terminal = logging.StreamHandler()
        handler_terminal.setFormatter(formato)

        logger.addHandler(handler_arquivo)
        logger.addHandler(handler_terminal)

    return logger