import streamlit as st
import pandas as pd
from conexao import conectar 

# =========================
# LISTAR
# =========================
def listar_arbitros():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_arbitro, nome_arbitro, pais_origem
        FROM arbitros
        ORDER BY nome_arbitro
    """)

    dados = cursor.fetchall()
    cursor.close()
    conexao.close()

    return pd.DataFrame(dados)


# =========================
# BUSCAR POR ID
# =========================
def buscar_arbitro(id_arbitro):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM arbitros
        WHERE id_arbitro = %s
    """, (id_arbitro,))

    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    return resultado


# =========================
# INSERIR
# =========================
def inserir_arbitro(nome, pais):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO arbitros
        (nome_arbitro, pais_origem)
        VALUES (%s, %s)
    """, (nome, pais))

    conexao.commit()
    cursor.close()
    conexao.close()


# =========================
# ATUALIZAR
# =========================
def atualizar_arbitro(id_arbitro, nome, pais):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE arbitros
        SET
            nome_arbitro = %s,
            pais_origem = %s
        WHERE id_arbitro = %s
    """, (nome, pais, id_arbitro))

    conexao.commit()
    cursor.close()
    conexao.close()


# =========================
# EXCLUIR
# =========================
def excluir_arbitro(id_arbitro):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM arbitros
        WHERE id_arbitro = %s
    """, (id_arbitro,))

    conexao.commit()
    cursor.close()
    conexao.close()


# ============================================
# TELA DE ÁRBITROS (EXECUÇÃO DIRETA)
# ============================================
st.header("🧑‍⚖️ Gerenciar Árbitros")

# Carregar dados
df = listar_arbitros()

aba1, aba2, aba3 = st.tabs(["Cadastrar", "Editar", "Excluir"])

# =========================
# CADASTRAR
# =========================
with aba1:
    st.subheader("Novo Árbitro")
    
    nome = st.text_input("Nome do Árbitro", key="a_nome")
    pais = st.text_input("País de Origem", key="a_pais")
    
    if st.button("Cadastrar Árbitro"):
        if nome and pais:
            inserir_arbitro(nome, pais)
            st.success("Árbitro cadastrado!")
            st.rerun()
        else:
            st.error("Por favor, preencha todos os campos.")

# =========================
# EDITAR
# =========================
with aba2:
    st.subheader("Editar Árbitro")
    
    if not df.empty:
        opcoes = {linha["nome_arbitro"]: linha["id_arbitro"] for _, linha in df.iterrows()}
        escolhido = st.selectbox("Árbitro", list(opcoes.keys()), key="edit_arbitro")
        registro = buscar_arbitro(opcoes[escolhido])
        
        nome_edit = st.text_input("Nome", value=registro["nome_arbitro"], key="edit_nome")
        pais_edit = st.text_input("País", value=registro["pais_origem"], key="edit_pais")
        
        if st.button("Atualizar Árbitro"):
            atualizar_arbitro(registro["id_arbitro"], nome_edit, pais_edit)
            st.success("Atualizado!")
            st.rerun()
    else:
        st.warning("Nenhum árbitro cadastrado.")

# =========================
# EXCLUIR
# =========================
with aba3:
    st.subheader("Excluir Árbitro")
    
    if not df.empty:
        opcoes = {linha["nome_arbitro"]: linha["id_arbitro"] for _, linha in df.iterrows()}
        escolhido = st.selectbox("Árbitro", list(opcoes.keys()), key="del_arbitro")
        
        if st.button("Excluir Árbitro"):
            excluir_arbitro(opcoes[escolhido])
            st.success("Árbitro removido!")
            st.rerun()
    else:
        st.warning("Nenhum árbitro cadastrado.")

# =========================
# TABELA DE ÁRBITROS
# =========================
st.divider()
st.subheader("📋 Lista de Árbitros")

if df.empty:
    st.warning("Nenhum árbitro cadastrado.")
else:
    # Renomeando as colunas no DataFrame para exibição mais bonita no Dashboard
    df_exibicao = df.rename(columns={
        "id_arbitro": "ID",
        "nome_arbitro": "Nome do Árbitro",
        "pais_origem": "País de Origem"
    })
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)