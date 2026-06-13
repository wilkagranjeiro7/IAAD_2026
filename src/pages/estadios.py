import streamlit as st
import pandas as pd
from conexao import conectar

# ==============================================================================
# SISTEMA DE DESIGN — MESMO PADRÃO DO DASHBOARD (LIGHT)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
    }

    .stApp { background-color: #FFFFFF; }

    [data-testid="stSidebar"] {
        background-color: #F5F7FA !important;
        border-right: 1px solid #E2E6EA !important;
    }
    [data-testid="stSidebar"] * { color: #555F6D !important; font-size: 0.95rem !important; }

    .dash-header {
        border-top: 4px solid #1A73E8;
        background: #F5F7FA;
        border-radius: 0 0 10px 10px;
        padding: 28px 36px 22px 36px;
        margin-bottom: 28px;
        border: 1px solid #E2E6EA;
        border-top: 4px solid #1A73E8;
    }
    .dash-header .eyebrow {
        font-size: 0.75rem; font-weight: 700; letter-spacing: 0.18em;
        text-transform: uppercase; color: #1A73E8; margin-bottom: 8px;
    }
    .dash-header h1 {
        font-size: 2rem !important; font-weight: 900; color: #1A1F2E !important;
        margin: 0 0 8px 0 !important; line-height: 1.2; letter-spacing: -0.02em;
    }
    .dash-header .sub { font-size: 0.9rem; color: #6B7280; font-weight: 400; }

    .kpi-card {
        background: #FFFFFF; border: 1px solid #E2E6EA; border-radius: 10px;
        padding: 22px 24px; text-align: left; position: relative;
        overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #1A73E8, #4DA3FF);
    }
    .kpi-card .kpi-icon { font-size: 1.6rem; margin-bottom: 10px; display: block; }
    .kpi-card .kpi-value {
        font-size: 2.4rem; font-weight: 900; color: #1A1F2E;
        line-height: 1; letter-spacing: -0.03em;
    }
    .kpi-card .kpi-label {
        font-size: 0.75rem; font-weight: 600; letter-spacing: 0.1em;
        text-transform: uppercase; color: #6B7280; margin-top: 8px;
    }

    .section-label {
        font-size: 0.75rem; font-weight: 700; letter-spacing: 0.15em;
        text-transform: uppercase; color: #1A73E8; margin-bottom: 6px;
    }

    .form-card {
        background: #FFFFFF; border: 1px solid #E2E6EA; border-radius: 10px;
        padding: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); margin-bottom: 8px;
    }
    .form-card-title {
        font-size: 1.0rem; font-weight: 700; color: #1A1F2E;
        margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
    }

    .table-card {
        background: #FFFFFF; border: 1px solid #E2E6EA; border-radius: 10px;
        padding: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .table-title {
        font-size: 1.0rem; font-weight: 700; color: #1A1F2E;
        margin-bottom: 14px; display: flex; align-items: center; gap: 8px;
    }

    .divider { border: none; border-top: 1px solid #E2E6EA; margin: 28px 0; }

    .stTextInput > div > div > input {
        border: 1px solid #D1D5DB !important; border-radius: 6px !important;
        font-size: 0.95rem !important; padding: 10px 12px !important; color: #1A1F2E !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1A73E8 !important;
        box-shadow: 0 0 0 3px rgba(26,115,232,0.12) !important;
    }

    .stNumberInput > div > div > input {
        border: 1px solid #D1D5DB !important; border-radius: 6px !important;
        font-size: 0.95rem !important; padding: 10px 12px !important; color: #1A1F2E !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #F5F7FA; border-radius: 8px; padding: 4px;
        gap: 4px; border: 1px solid #E2E6EA; margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px !important; font-size: 0.9rem !important;
        font-weight: 600 !important; color: #6B7280 !important; padding: 8px 20px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important; color: #1A73E8 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    .stSelectbox > div > div {
        border: 1px solid #D1D5DB !important; border-radius: 6px !important;
        font-size: 0.95rem !important;
    }

    .stButton > button {
        background-color: #1A73E8 !important; color: #FFFFFF !important;
        border: none !important; border-radius: 6px !important;
        font-size: 0.9rem !important; font-weight: 600 !important;
        padding: 10px 22px !important; transition: background 0.2s !important;
    }
    .stButton > button:hover { background-color: #1557B0 !important; }

    .btn-danger > button { background-color: #EF4444 !important; }
    .btn-danger > button:hover { background-color: #DC2626 !important; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES DE CONSULTA
# ==============================================================================

def listar_estadios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_estadio, nome_estadio, cidade, pais, capacidade FROM estadios ORDER BY nome_estadio")
    dados = cursor.fetchall()
    cursor.close(); conexao.close()
    return pd.DataFrame(dados)

def buscar_estadio(id_estadio):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estadios WHERE id_estadio = %s", (id_estadio,))
    resultado = cursor.fetchone()
    cursor.close(); conexao.close()
    return resultado

def inserir_estadio(nome, cidade, pais, capacidade):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO estadios (nome_estadio, cidade, pais, capacidade) VALUES (%s, %s, %s, %s)", (nome, cidade, pais, capacidade))
    conexao.commit(); cursor.close(); conexao.close()

def atualizar_estadio(id_estadio, nome, cidade, pais, capacidade):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE estadios SET nome_estadio=%s, cidade=%s, pais=%s, capacidade=%s WHERE id_estadio=%s", (nome, cidade, pais, capacidade, id_estadio))
    conexao.commit(); cursor.close(); conexao.close()

def excluir_estadio(id_estadio):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM estadios WHERE id_estadio = %s", (id_estadio,))
    conexao.commit(); cursor.close(); conexao.close()

# ==============================================================================
# INTERFACE
# ==============================================================================

df = listar_estadios()
total_estadios  = len(df)
total_paises    = df["pais"].nunique() if not df.empty else 0
maior_cap       = f"{int(df['capacidade'].max()):,}".replace(",", ".") if not df.empty else "—"

# HEADER
st.markdown("""
<div class="dash-header">
    <div class="eyebrow">🏟️ Infraestrutura</div>
    <h1>Estádios</h1>
    <div class="sub">Cadastro, edição e remoção dos estádios utilizados no torneio</div>
</div>
""", unsafe_allow_html=True)

# KPIs
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🏟️</span>
        <div class="kpi-value">{total_estadios}</div>
        <div class="kpi-label">Estádios cadastrados</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🌍</span>
        <div class="kpi-value">{total_paises}</div>
        <div class="kpi-label">Países sede</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">👥</span>
        <div class="kpi-value" style="font-size:1.8rem">{maior_cap}</div>
        <div class="kpi-label">Maior capacidade</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ABAS DE CRUD
st.markdown('<div class="section-label">Gerenciamento</div>', unsafe_allow_html=True)

aba1, aba2, aba3 = st.tabs(["➕  Cadastrar", "✏️  Editar", "🗑️  Excluir"])

with aba1:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">➕ Novo Estádio</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        nome      = st.text_input("Nome do Estádio", key="e_nome", placeholder="Ex: Maracanã")
        cidade    = st.text_input("Cidade", key="e_cidade", placeholder="Ex: Rio de Janeiro")
    with col2:
        pais      = st.text_input("País", key="e_pais", placeholder="Ex: Brasil")
        capacidade = st.number_input("Capacidade", min_value=0, key="e_capacidade")
    if st.button("Cadastrar Estádio", key="btn_cadastrar"):
        if nome and cidade and pais and capacidade > 0:
            inserir_estadio(nome, cidade, pais, capacidade)
            st.success("✅ Estádio cadastrado com sucesso!")
            st.rerun()
        else:
            st.error("Preencha todos os campos corretamente antes de cadastrar.")
    st.markdown('</div>', unsafe_allow_html=True)

with aba2:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">✏️ Editar Estádio</div>', unsafe_allow_html=True)
    if not df.empty:
        opcoes    = {linha["nome_estadio"]: linha["id_estadio"] for _, linha in df.iterrows()}
        escolhido = st.selectbox("Selecione o estádio", list(opcoes.keys()), key="edit_estadio")
        registro  = buscar_estadio(opcoes[escolhido])
        col1, col2 = st.columns(2)
        with col1:
            nome_edit     = st.text_input("Nome", value=registro["nome_estadio"], key="edit_nome")
            cidade_edit   = st.text_input("Cidade", value=registro["cidade"], key="edit_cidade")
        with col2:
            pais_edit     = st.text_input("País", value=registro["pais"], key="edit_pais")
            capacidade_edit = st.number_input("Capacidade", value=int(registro["capacidade"]), min_value=0, key="edit_capacidade")
        if st.button("Salvar alterações", key="btn_editar"):
            atualizar_estadio(registro["id_estadio"], nome_edit, cidade_edit, pais_edit, capacidade_edit)
            st.success("✅ Estádio atualizado com sucesso!")
            st.rerun()
    else:
        st.warning("Nenhum estádio cadastrado ainda.")
    st.markdown('</div>', unsafe_allow_html=True)

with aba3:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">🗑️ Remover Estádio</div>', unsafe_allow_html=True)
    if not df.empty:
        opcoes    = {linha["nome_estadio"]: linha["id_estadio"] for _, linha in df.iterrows()}
        escolhido = st.selectbox("Selecione o estádio", list(opcoes.keys()), key="del_estadio")
        st.warning(f"Você está prestes a remover **{escolhido}** permanentemente.")
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("Confirmar exclusão", key="btn_excluir"):
            excluir_estadio(opcoes[escolhido])
            st.success("✅ Estádio removido.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Nenhum estádio cadastrado ainda.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# TABELA
st.markdown('<div class="section-label">Registros</div>', unsafe_allow_html=True)
st.markdown('<div class="table-card">', unsafe_allow_html=True)
st.markdown('<div class="table-title">📋 Lista completa de estádios</div>', unsafe_allow_html=True)
if df.empty:
    st.info("Nenhum estádio cadastrado.")
else:
    df_exibicao = df.rename(columns={
        "id_estadio":   "ID",
        "nome_estadio": "Nome do Estádio",
        "cidade":       "Cidade",
        "pais":         "País",
        "capacidade":   "Capacidade"
    })
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# SIDEBAR
st.sidebar.markdown("### PROJETO")
st.sidebar.markdown("**Banco de Dados I**\nSistemas de Informação")
st.sidebar.markdown("---")
st.sidebar.markdown("### EQUIPE")
for autor in [
    "Arthur Ferreira Barbosa", "Guilherme Nery Rocha",
    "Isadora Morais", "Kassiane Gomes da Silva",
    "Leandro Augusto Barboza da Silva", "Wilka Vitória G. do Nascimento"
]:
    st.sidebar.markdown(f"· {autor}")