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

    /* Barra de progresso dos grupos */
    .progress-wrap {
        background: #FFFFFF; border: 1px solid #E2E6EA; border-radius: 10px;
        padding: 22px 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .progress-label {
        font-size: 0.78rem; font-weight: 600; color: #6B7280;
        text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px;
    }
    .progress-bar-bg {
        background: #F0F2F5; border-radius: 99px; height: 12px; width: 100%;
    }
    .progress-bar-fill {
        height: 12px; border-radius: 99px;
        transition: width 0.4s ease;
    }
    .progress-count {
        font-size: 0.82rem; color: #6B7280; margin-top: 8px;
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

    .stButton > button {
        background-color: #1A73E8 !important; color: #FFFFFF !important;
        border: none !important; border-radius: 6px !important;
        font-size: 0.9rem !important; font-weight: 600 !important;
        padding: 10px 22px !important; transition: background 0.2s !important;
    }
    .stButton > button:hover { background-color: #1557B0 !important; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES DE CONSULTA
# ==============================================================================

def listar_grupos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_grupo, nome_grupo FROM grupos ORDER BY nome_grupo")
    dados = cursor.fetchall()
    cursor.close(); conexao.close()
    return pd.DataFrame(dados)

def inserir_grupo(nome_grupo):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO grupos (nome_grupo) VALUES (%s)", (nome_grupo,))
    conexao.commit(); cursor.close(); conexao.close()

# ==============================================================================
# INTERFACE
# ==============================================================================

TOTAL_GRUPOS = 12
df = listar_grupos()
cadastrados  = len(df)
faltam       = max(0, TOTAL_GRUPOS - cadastrados)
pct          = min(100, int((cadastrados / TOTAL_GRUPOS) * 100))

# Cor da barra de progresso
if cadastrados < TOTAL_GRUPOS:
    bar_color = "#1A73E8"
elif cadastrados == TOTAL_GRUPOS:
    bar_color = "#16A34A"
else:
    bar_color = "#EF4444"

# HEADER
st.markdown("""
<div class="dash-header">
    <div class="eyebrow">🏆 Estrutura do Torneio</div>
    <h1>Grupos</h1>
    <div class="sub">Cadastro e visualização dos grupos da Copa do Mundo 2026</div>
</div>
""", unsafe_allow_html=True)

# KPIs + PROGRESSO
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🏆</span>
        <div class="kpi-value">{cadastrados}</div>
        <div class="kpi-label">Grupos cadastrados</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⏳</span>
        <div class="kpi-value">{faltam}</div>
        <div class="kpi-label">Grupos faltando</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label">Progresso — {cadastrados} de {TOTAL_GRUPOS} grupos</div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{pct}%; background:{bar_color};"></div>
        </div>
        <div class="progress-count">{pct}% completo</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# LAYOUT: FORMULÁRIO + TABELA
st.markdown('<div class="section-label">Gerenciamento</div>', unsafe_allow_html=True)

col_form, col_table = st.columns([1, 1], gap="large")

with col_form:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">➕ Novo Grupo</div>', unsafe_allow_html=True)

    nome = st.text_input("Nome do Grupo", key="g_nome", placeholder="Ex: A, B, C...")
    st.caption("A Copa do Mundo 2026 possui 12 grupos — de A a L.")

    if st.button("Cadastrar Grupo", key="btn_cadastrar"):
        if nome.strip():
            inserir_grupo(nome.strip().upper())
            st.success(f"✅ Grupo {nome.strip().upper()} cadastrado com sucesso!")
            st.rerun()
        else:
            st.error("Digite um nome para o grupo antes de cadastrar.")

    # Status inline após o botão
    st.markdown("<br>", unsafe_allow_html=True)
    if cadastrados == TOTAL_GRUPOS:
        st.success("🎉 Todos os 12 grupos estão cadastrados!")
    elif cadastrados > TOTAL_GRUPOS:
        st.error(f"❌ Há {cadastrados} grupos — a Copa 2026 prevê apenas {TOTAL_GRUPOS}.")

    st.markdown('</div>', unsafe_allow_html=True)

with col_table:
    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.markdown('<div class="table-title">📋 Grupos cadastrados</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("Nenhum grupo cadastrado ainda.")
    else:
        df_exibicao = df.rename(columns={"id_grupo": "ID", "nome_grupo": "Grupo"})
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