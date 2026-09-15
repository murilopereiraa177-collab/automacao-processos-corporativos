import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.utils.logger import configurar_logger

logger = configurar_logger("selenium")


def preencher_formulario(fornecedor):
    """
    Abre o navegador, preenche o formulário de cadastro do webapp_demo
    e verifica se a mensagem de sucesso apareceu.
    'fornecedor' deve ser um dicionário com: nome, cnpj, categoria
    """
    driver = webdriver.Chrome()

    try:
        driver.get("http://127.0.0.1:5000")

        campo_nome = driver.find_element(By.ID, "nome")
        campo_nome.send_keys(fornecedor["nome"])

        campo_cnpj = driver.find_element(By.ID, "cnpj")
        campo_cnpj.send_keys(fornecedor["cnpj"])

        select_categoria = driver.find_element(By.ID, "categoria")
        select_categoria.send_keys(fornecedor["categoria"])

        botao_salvar = driver.find_element(By.ID, "btn-salvar")
        botao_salvar.click()

        time.sleep(1)  # espera a página recarregar com a mensagem

        mensagem = driver.find_element(By.ID, "mensagem-sucesso")
        sucesso = "sucesso" in mensagem.text.lower()

        if sucesso:
            logger.info(f"Formulário preenchido com sucesso para o CNPJ {fornecedor['cnpj']}")
        else:
            logger.warning(f"Formulário preenchido, mas mensagem de sucesso não confirmada para o CNPJ {fornecedor['cnpj']}")

        return sucesso

    except Exception as erro:
        logger.error(f"Erro ao preencher formulário para o CNPJ {fornecedor.get('cnpj', '?')}: {erro}")
        return False

    finally:
        time.sleep(2)
        driver.quit()


# Teste rápido
if __name__ == "__main__":
    fornecedor_teste = {
        "nome": "Empresa Teste Selenium LTDA",
        "cnpj": "11.111.111/0001-11",
        "categoria": "Fornecedor Geral",
    }

    resultado = preencher_formulario(fornecedor_teste)
    print("Sucesso!" if resultado else "Falhou.")