import streamlit as st
import pandas as pd
from conexao import conectar  

# =========================
# LISTAR
# =========================
def listar_grupos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_grupo, nome_grupo
        FROM grupos
        ORDER BY nome_grupo
    """)

    dados = cursor.fetchall()
    cursor.close()
    conexao.close()

    return pd.DataFrame(dados)


# =========================
# INSERIR
# =========================
def inserir_grupo(nome_grupo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO grupos (nome_grupo)
        VALUES (%s)
    """, (nome_grupo,))

    conexao.commit()
    cursor.close()
    conexao.close()


# ============================================
# TELA DE GRUPOS (EXECUÇÃO DIRETA)
# ============================================
# CORRIGIDO: Retirado o def tela_grupos() e o botão voltar manual.
# O Dashboard executa este script diretamente ao clicar na aba.

st.header("🏆 Grupos da Copa")

# Carregar dados
df = listar_grupos()

col1, col2 = st.columns(2)

# =========================
# CADASTRAR NOVO GRUPO
# =========================
with col1:
    st.subheader("Novo Grupo")
    
    nome = st.text_input("Nome do Grupo (A, B, C...)")
    
    if st.button("Cadastrar Grupo"):
        if nome.strip():
            inserir_grupo(nome.upper())
            st.success(f"Grupo {nome.upper()} cadastrado!")
            st.rerun()
        else:
            st.error("Digite um nome para o grupo!")

# =========================
# LISTAR GRUPOS
# =========================
with col2:
    st.subheader("Grupos Cadastrados")
    
    if df.empty:
        st.warning("Nenhum grupo cadastrado.")
    else:
        # Deixando os nomes das colunas legíveis para o usuário final
        df_exibicao = df.rename(columns={
            "id_grupo": "ID",
            "nome_grupo": "Grupo"
        })
        st.dataframe(df_exibicao, use_container_width=True, hide_index=True)

# =========================
# INFORMAÇÃO ADICIONAL
# =========================
st.divider()
st.info("💡 Os grupos devem ser de A a L (12 grupos no total para a Copa 2026)")

# Mostrar quantos grupos estão cadastrados
if not df.empty:
    st.success(f"✅ Total de grupos cadastrados: {len(df)} de 12")
    
    if len(df) < 12:
        faltam = 12 - len(df)
        st.warning(f"⚠️ Faltam {faltam} grupo(s) para completar a Copa 2026")
    elif len(df) == 12:
        st.success("🎉 Perfeito! Todos os 12 grupos estão cadastrados!")
    else:
        st.error(f"❌ Você tem {len(df)} grupos cadastrados, mas a Copa 2026 tem apenas 12 grupos!")