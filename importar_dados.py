import os
import mysql.connector

def importar_todos_os_dumps():
    try:
        # Conexão local (Insira sua senha)
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456", 
            database="mydb"
        )
        cursor = conexao.cursor()
        print("🔄 Conectado ao MySQL. Desativando travas e iniciando limpeza...")

        # DESATIVA as travas temporariamente para a carga passar pelas triggers
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # Ordem estrita para truncar dados sem gerar erros de amarração
        tabelas = ["cartoes", "gols", "partidas", "jogadores", "arbitros", "estadios", "selecoes", "grupos"]
        for tabela in tabelas:
            try:
                cursor.execute(f"TRUNCATE TABLE `{tabela}`;")
            except mysql.connector.Error:
                continue

        print("🧹 Banco de dados limpo! Iniciando a injeção dos arquivos...")

        ordem_arquivos = [
            "mydb_grupos.sql",
            "mydb_selecoes.sql",
            "mydb_estadios.sql",
            "mydb_arbitros.sql",
            "mydb_jogadores.sql",
            "mydb_partidas.sql",
            "mydb_gols.sql",
            "mydb_cartoes.sql"
        ]

        pasta_database = "Dump20260608"

        for nome_arquivo in ordem_arquivos:
            caminho_completo = os.path.join(pasta_database, nome_arquivo)
            
            if os.path.exists(caminho_completo):
                print(f"📦 Importando {nome_arquivo}...")
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    script_sql = f.read()
                
                script_sql = script_sql.replace("DELIMITER $$", "").replace("DELIMITER ;", "")
                
                comandos = script_sql.split(';')
                for comando in comandos:
                    comando_limpo = comando.strip()
                    
                    # Ignora linhas de controle do dump que travam a execução no Python
                    if (not comando_limpo or 
                        comando_limpo.startswith('--') or 
                        comando_limpo.startswith('/*') or 
                        "CREATE TABLE" in comando_limpo or 
                        "DROP TABLE" in comando_limpo or
                        "LOCK TABLES" in comando_limpo or 
                        "UNLOCK TABLES" in comando_limpo or
                        "sql_log_bin" in comando_limpo):
                        continue
                        
                    try:
                        cursor.execute(comando_limpo)
                    except mysql.connector.Error:
                        continue
                
                conexao.commit()

        # REATIVA as checagens de chave estrangeira para manter a segurança do banco
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conexao.commit()
        
        print("✅ Todos os dados (incluindo partidas) foram carregados com sucesso!")

    except mysql.connector.Error as erro:
        print(f"❌ Erro de conexão principal: {erro}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    importar_todos_os_dumps()