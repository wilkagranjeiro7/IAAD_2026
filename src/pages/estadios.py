import streamlit as st
import pandas as pd
from conexao import conectar  

# =========================
# LISTAR
# =========================
def listar_estadios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_estadio, nome_estadio, cidade, pais, capacidade
        FROM estadios
        ORDER BY nome_estadio
    """)

    dados = cursor.fetchall()
    cursor.close()
    conexao.close()

    return pd.DataFrame(dados)


# =========================
# BUSCAR POR ID
# =========================
def buscar_estadio(id_estadio):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM estadios
        WHERE id_estadio = %s
    """, (id_estadio,))

    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    return resultado


# =========================
# INSERIR
# =========================
def inserir_estadio(nome, cidade, pais, capacidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO estadios
        (nome_estadio, cidade, pais, capacidade)
        VALUES (%s, %s, %s, %s)
    """, (nome, cidade, pais, capacidade))

    conexao.commit()
    cursor.close()
    conexao.close()


# =========================
# ATUALIZAR
# =========================
def atualizar_estadio(id_estadio, nome, cidade, pais, capacidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE estadios
        SET
            nome_estadio = %s,
            cidade = %s,
            pais = %s,
            capacidade = %s
        WHERE id_estadio = %s
    """, (nome, cidade, pais, capacidade, id_estadio))

    conexao.commit()
    cursor.close()
    conexao.close()


# =========================
# EXCLUIR
# =========================
def excluir_estadio(id_estadio):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM estadios
        WHERE id_estadio = %s
    """, (id_estadio,))

    conexao.commit()
    cursor.close()
    conexao.close()


# ============================================
# TELA DE ESTÁDIOS (EXECUÇÃO DIRETA)
# ============================================
# CORRIGIDO: Retirado o def tela_estadios() e o botão voltar manual.
# O Streamlit executa esse arquivo direto e monta o menu lateral sozinho.

st.header("🏟️ Gerenciar Estádios")

# Carregar dados
df = listar_estadios()

aba1, aba2, aba3 = st.tabs(["Cadastrar", "Editar", "Excluir"])

# =========================
# CADASTRAR
# =========================
with aba1:
    st.subheader("Novo Estádio")
    
    nome = st.text_input("Nome do Estádio", key="e_nome")
    cidade = st.text_input("Cidade", key="e_cidade")
    pais = st.text_input("País", key="e_pais")
    capacidade = st.number_input("Capacidade", min_value=0, key="e_capacidade")
    
    if st.button("Cadastrar Estádio"):
        if nome and cidade and pais and capacidade > 0:
            inserir_estadio(nome, cidade, pais, capacidade)
            st.success("Estádio cadastrado!")
            st.rerun()
        else:
            st.error("Por favor, preencha todos os campos corretamente.")

# =========================
# EDITAR
# =========================
with aba2:
    st.subheader("Editar Estádio")
    
    if not df.empty:
        opcoes = {linha["nome_estadio"]: linha["id_estadio"] for _, linha in df.iterrows()}
        escolhido = st.selectbox("Estádio", list(opcoes.keys()), key="edit_estadio")
        registro = buscar_estadio(opcoes[escolhido])
        
        nome_edit = st.text_input("Nome", value=registro["nome_estadio"], key="edit_nome")
        cidade_edit = st.text_input("Cidade", value=registro["cidade"], key="edit_cidade")
        pais_edit = st.text_input("País", value=registro["pais"], key="edit_pais")
        capacidade_edit = st.number_input("Capacidade", value=int(registro["capacidade"]), min_value=0, key="edit_capacidade")
        
        if st.button("Atualizar Estádio"):
            atualizar_estadio(registro["id_estadio"], nome_edit, cidade_edit, pais_edit, capacidade_edit)
            st.success("Atualizado!")
            st.rerun()
    else:
        st.warning("Nenhum estádio cadastrado.")

# =========================
# EXCLUIR
# =========================
with aba3:
    st.subheader("Excluir Estádio")
    
    if not df.empty:
        opcoes = {linha["nome_estadio"]: linha["id_estadio"] for _, linha in df.iterrows()}
        escolhido = st.selectbox("Estádio", list(opcoes.keys()), key="del_estadio")
        
        if st.button("Excluir Estádio"):
            excluir_estadio(opcoes[escolhido])
            st.success("Estádio removido!")
            st.rerun()
    else:
        st.warning("Nenhum estádio cadastrado.")

# =========================
# TABELA DE ESTÁDIOS
# =========================
st.divider()
st.subheader("📋 Lista de Estádios")

if df.empty:
    st.warning("Nenhum estádio cadastrado.")
else:
    # CORRIGIDO: Exibição mais limpa e com títulos bonitos na tabela
    df_exibicao = df.rename(columns={
        "id_estadio": "ID",
        "nome_estadio": "Nome do Estádio",
        "cidade": "Cidade",
        "pais": "País",
        "capacidade": "Capacidade"
    })
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)