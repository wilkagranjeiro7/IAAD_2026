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

    .stApp {
        background-color: #FFFFFF;
    }

    [data-testid="stSidebar"] {
        background-color: #F5F7FA !important;
        border-right: 1px solid #E2E6EA !important;
    }
    [data-testid="stSidebar"] * {
        color: #555F6D !important;
        font-size: 0.95rem !important;
    }

    /* Header da página */
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
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #1A73E8;
        margin-bottom: 8px;
    }
    .dash-header h1 {
        font-size: 2rem !important;
        font-weight: 900;
        color: #1A1F2E !important;
        margin: 0 0 8px 0 !important;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    .dash-header .sub {
        font-size: 0.9rem;
        color: #6B7280;
        font-weight: 400;
    }

    /* Cards KPI */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E6EA;
        border-radius: 10px;
        padding: 22px 24px;
        text-align: left;
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #1A73E8, #4DA3FF);
    }
    .kpi-card .kpi-icon { font-size: 1.6rem; margin-bottom: 10px; display: block; }
    .kpi-card .kpi-value {
        font-size: 2.4rem;
        font-weight: 900;
        color: #1A1F2E;
        line-height: 1;
        letter-spacing: -0.03em;
    }
    .kpi-card .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6B7280;
        margin-top: 8px;
    }

    /* Seção label */
    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #1A73E8;
        margin-bottom: 6px;
    }

    /* Card de formulário */
    .form-card {
        background: #FFFFFF;
        border: 1px solid #E2E6EA;
        border-radius: 10px;
        padding: 24px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        margin-bottom: 8px;
    }
    .form-card-title {
        font-size: 1.0rem;
        font-weight: 700;
        color: #1A1F2E;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Card tabela */
    .table-card {
        background: #FFFFFF;
        border: 1px solid #E2E6EA;
        border-radius: 10px;
        padding: 24px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .table-title {
        font-size: 1.0rem;
        font-weight: 700;
        color: #1A1F2E;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Divisor */
    .divider {
        border: none;
        border-top: 1px solid #E2E6EA;
        margin: 28px 0;
    }

    /* Inputs com mais destaque */
    .stTextInput > div > div > input {
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
        padding: 10px 12px !important;
        color: #1A1F2E !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1A73E8 !important;
        box-shadow: 0 0 0 3px rgba(26,115,232,0.12) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F5F7FA;
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #E2E6EA;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #6B7280 !important;
        padding: 8px 20px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #1A73E8 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
    }

    /* Botões */
    .stButton > button {
        background-color: #1A73E8 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        padding: 10px 22px !important;
        transition: background 0.2s !important;
    }
    .stButton > button:hover {
        background-color: #1557B0 !important;
    }

    /* Botão de excluir — vermelho */
    .btn-danger > button {
        background-color: #EF4444 !important;
    }
    .btn-danger > button:hover {
        background-color: #DC2626 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES DE CONSULTA
# ==============================================================================

def listar_arbitros():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_arbitro, nome_arbitro, pais_origem FROM arbitros ORDER BY nome_arbitro")
    dados = cursor.fetchall()
    cursor.close(); conexao.close()
    return pd.DataFrame(dados)

def buscar_arbitro(id_arbitro):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM arbitros WHERE id_arbitro = %s", (id_arbitro,))
    resultado = cursor.fetchone()
    cursor.close(); conexao.close()
    return resultado

def inserir_arbitro(nome, pais):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO arbitros (nome_arbitro, pais_origem) VALUES (%s, %s)", (nome, pais))
    conexao.commit(); cursor.close(); conexao.close()

def atualizar_arbitro(id_arbitro, nome, pais):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE arbitros SET nome_arbitro = %s, pais_origem = %s WHERE id_arbitro = %s", (nome, pais, id_arbitro))
    conexao.commit(); cursor.close(); conexao.close()

def excluir_arbitro(id_arbitro):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM arbitros WHERE id_arbitro = %s", (id_arbitro,))
    conexao.commit(); cursor.close(); conexao.close()

# ==============================================================================
# INTERFACE
# ==============================================================================

df = listar_arbitros()
total_arbitros = len(df)
paises_unicos = df["pais_origem"].nunique() if not df.empty else 0

# HEADER
st.markdown("""
<div class="dash-header">
    <div class="eyebrow">🧑‍⚖️ Gestão de Pessoal</div>
    <h1>Árbitros</h1>
    <div class="sub">Cadastro, edição e remoção de árbitros registrados no torneio</div>
</div>
""", unsafe_allow_html=True)

# KPIs
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🧑‍⚖️</span>
        <div class="kpi-value">{total_arbitros}</div>
        <div class="kpi-label">Árbitros cadastrados</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🌍</span>
        <div class="kpi-value">{paises_unicos}</div>
        <div class="kpi-label">Países representados</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    ultimo = df["nome_arbitro"].iloc[-1] if not df.empty else "—"
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🆕</span>
        <div class="kpi-value" style="font-size:1.2rem; padding-top:6px">{ultimo}</div>
        <div class="kpi-label">Último cadastrado</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ABAS DE CRUD
st.markdown('<div class="section-label">Gerenciamento</div>', unsafe_allow_html=True)

aba1, aba2, aba3 = st.tabs(["➕  Cadastrar", "✏️  Editar", "🗑️  Excluir"])

with aba1:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">➕ Novo Árbitro</div>', unsafe_allow_html=True)
    nome = st.text_input("Nome do Árbitro", key="a_nome", placeholder="Ex: Sandro Ricci")
    pais = st.text_input("País de Origem", key="a_pais", placeholder="Ex: Brasil")
    if st.button("Cadastrar Árbitro", key="btn_cadastrar"):
        if nome and pais:
            inserir_arbitro(nome, pais)
            st.success("✅ Árbitro cadastrado com sucesso!")
            st.rerun()
        else:
            st.error("Preencha todos os campos antes de cadastrar.")
    st.markdown('</div>', unsafe_allow_html=True)

with aba2:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">✏️ Editar Árbitro</div>', unsafe_allow_html=True)
    if not df.empty:
        opcoes = {linha["nome_arbitro"]: linha["id_arbitro"] for _, linha in df.iterrows()}
        escolhido = st.selectbox("Selecione o árbitro", list(opcoes.keys()), key="edit_arbitro")
        registro = buscar_arbitro(opcoes[escolhido])
        nome_edit = st.text_input("Nome", value=registro["nome_arbitro"], key="edit_nome")
        pais_edit = st.text_input("País", value=registro["pais_origem"], key="edit_pais")
        if st.button("Salvar alterações", key="btn_editar"):
            atualizar_arbitro(registro["id_arbitro"], nome_edit, pais_edit)
            st.success("✅ Dados atualizados com sucesso!")
            st.rerun()
    else:
        st.warning("Nenhum árbitro cadastrado ainda.")
    st.markdown('</div>', unsafe_allow_html=True)

with aba3:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">🗑️ Remover Árbitro</div>', unsafe_allow_html=True)
    if not df.empty:
        opcoes = {linha["nome_arbitro"]: linha["id_arbitro"] for _, linha in df.iterrows()}
        escolhido = st.selectbox("Selecione o árbitro", list(opcoes.keys()), key="del_arbitro")
        st.warning(f"Você está prestes a remover **{escolhido}** permanentemente.")
        with st.container():
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button("Confirmar exclusão", key="btn_excluir"):
                excluir_arbitro(opcoes[escolhido])
                st.success("✅ Árbitro removido.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Nenhum árbitro cadastrado ainda.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# TABELA
st.markdown('<div class="section-label">Registros</div>', unsafe_allow_html=True)
st.markdown('<div class="table-card">', unsafe_allow_html=True)
st.markdown('<div class="table-title">📋 Lista completa de árbitros</div>', unsafe_allow_html=True)
if df.empty:
    st.info("Nenhum árbitro cadastrado.")
else:
    df_exibicao = df.rename(columns={
        "id_arbitro": "ID",
        "nome_arbitro": "Nome do Árbitro",
        "pais_origem": "País de Origem"
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