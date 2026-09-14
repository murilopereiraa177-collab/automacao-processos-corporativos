import pandas as pd
import os

# Lista de solicitações fictícias de fornecedores
dados = [
    {"nome": "Comercial Silva Ltda", "cnpj": "12.345.678/0001-90", "email": "contato@silva.com.br", "categoria": "Material de Escritório", "valor_estimado": 5000.00},
    {"nome": "Tech Solutions ME", "cnpj": "98.765.432/0001-10", "email": "vendas@techsolutions.com", "categoria": "Tecnologia", "valor_estimado": 25000.00},
    {"nome": "Alimentos Bom Sabor", "cnpj": "11.222.333/0001-44", "email": "financeiro@bomsabor.com.br", "categoria": "Alimentação", "valor_estimado": 8000.00},
    {"nome": "Construtora Alicerce", "cnpj": "cnpj_invalido_123", "email": "obras@alicerce.com.br", "categoria": "Construção", "valor_estimado": 150000.00},
    {"nome": "Papelaria Central", "cnpj": "22.333.444/0001-55", "email": "papelariacentral_sem_arroba", "categoria": "Material de Escritório", "valor_estimado": 3000.00},
    {"nome": "Transportes Rápido", "cnpj": "33.444.555/0001-66", "email": "contato@rapido.com.br", "categoria": "Logística", "valor_estimado": 12000.00},
    {"nome": "", "cnpj": "44.555.666/0001-77", "email": "semnome@fornecedor.com.br", "categoria": "Consultoria", "valor_estimado": 20000.00},
    {"nome": "Móveis Planejados JR", "cnpj": "55.666.777/0001-88", "email": "jr@moveisplanejados.com.br", "categoria": "Móveis", "valor_estimado": 45000.00},
    {"nome": "Gráfica Rápida", "cnpj": "66.777.888/0001-99", "email": "grafica@rapida.com.br", "categoria": "Gráfica", "valor_estimado": 6500.00},
    {"nome": "Segurança Total EPI", "cnpj": "77.888.999/0001-00", "email": "seguranca@total.com.br", "categoria": "Segurança do Trabalho", "valor_estimado": 9800.00},
    {"nome": "Limpeza & Cia", "cnpj": "88.999.000/0001-11", "email": "limpeza@cia.com.br", "categoria": "Limpeza", "valor_estimado": 4200.00},
    {"nome": "Eletro Peças SP", "cnpj": "99.000.111/0001-22", "email": "vendas@eletropecas.com.br", "categoria": "Elétrica", "valor_estimado": 18500.00},
]

# Cria o DataFrame (a tabela) com o Pandas
df = pd.DataFrame(dados)

# Garante que a pasta data/input existe
os.makedirs("data/input", exist_ok=True)

# Salva como Excel
caminho = "data/input/solicitacoes.xlsx"
df.to_excel(caminho, index=False)

print(f"Planilha criada com sucesso em: {caminho}")
print(f"Total de registros: {len(df)}")