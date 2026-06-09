from IAAD_2026.src.conexao import conectar

try:
    conexao = conectar()

    if conexao.is_connected():
        print("Conectado ao MySQL com sucesso!")

    conexao.close()

except Exception as erro:
    print("Erro:", erro)