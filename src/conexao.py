import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",     # <- AJUSTE A SENHA do seu MySQL local
        database="mydb"   
    )

    return conexao