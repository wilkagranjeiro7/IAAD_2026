from IAAD_2026.src.conexao import conectar

conexao = conectar()
cursor = conexao.cursor(dictionary=True)

# Teste 1: Verificar se a tabela selecoes tem dados
cursor.execute("SELECT COUNT(*) as total FROM selecoes")
print("Total de seleções:", cursor.fetchone())

# Teste 2: Verificar se a tabela grupos tem dados
cursor.execute("SELECT COUNT(*) as total FROM grupos")
print("Total de grupos:", cursor.fetchone())

# Teste 3: Verificar os ids_grupo que existem
cursor.execute("SELECT DISTINCT id_grupo FROM selecoes ORDER BY id_grupo")
print("IDs de grupo nas seleções:", cursor.fetchall())

# Teste 4: Verificar os grupos disponíveis
cursor.execute("SELECT id_grupo, nome_grupo FROM grupos ORDER BY id_grupo")
print("Grupos na tabela:", cursor.fetchall())

# Teste 5: Fazer a consulta completa
cursor.execute("""
    SELECT 
        s.id_selecao,
        s.nome_selecao,
        s.continente,
        s.tecnico,
        s.titulos,
        s.id_grupo as selecao_id_grupo,
        g.id_grupo as grupo_id_grupo,
        g.nome_grupo
    FROM selecoes s
    LEFT JOIN grupos g ON s.id_grupo = g.id_grupo
    LIMIT 5
""")

print("\nPrimeiras 5 seleções:")
for row in cursor.fetchall():
    print(row)

cursor.close()
conexao.close()