from IAAD_2026.src.conexao import conectar

conexao = conectar()
cursor = conexao.cursor()

cursor.execute("SHOW TABLES")

for tabela in cursor.fetchall():
    print(tabela[0])

cursor.close()
conexao.close()