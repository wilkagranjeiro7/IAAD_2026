import streamlit as st
import pandas as pd
import mysql.connector
from conexao import conectar 

st.set_page_config(
    page_title="Copa do Mundo 2026 · Gerenciamento",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# SISTEMA DE DESIGN — PALETA BRANCA / LIGHT (CONECTADO AO DASHBOARD)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
    }

    /* Fundo branco */
    .stApp {
        background-color: #FFFFFF;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F5F7FA !important;
        border-right: 1px solid #E2E6EA !important;
    }
    [data-testid="stSidebar"] * {
        color: #555F6D !important;
        font-size: 0.95rem !important;
    }

    /* Header Mapeado no Padrão do Grupo */
    .dash-header {
        border-top: 4px solid #1A73E8;
        background: #F5F7FA;
        border-radius: 0 0 10px 10px;
        padding: 28px 36px 22px 36px;
        margin-bottom: 28px;
        border: 1px solid #E2E6EA;
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

    /* Seções e Cards Operacionais do CRUD */
    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #1A73E8;
        margin-bottom: 16px;
    }
    .operation-card {
        background: #FFFFFF;
        border: 1px solid #E2E6EA;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .operation-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1A1F2E;
        margin-bottom: 4px;
    }
    .operation-sub {
        font-size: 0.85rem;
        color: #6B7280;
        margin-bottom: 18px;
    }

    /* Inputs Customizados */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        border: 1px solid #D1D5DB !important; border-radius: 6px !important;
        font-size: 0.95rem !important; padding: 10px 12px !important; color: #1A1F2E !important;
    }
    .stSelectbox > div > div {
        border: 1px solid #D1D5DB !important; border-radius: 6px !important;
    }

    /* Abas customizadas */
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

    /* Botões Padrão e Perigo */
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
# FUNÇÕES DE CONSULTA E BANCO DE DADOS (CRUD)
# ==============================================================================
def buscar_selecoes_aux():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_selecao, nome_selecao FROM selecoes ORDER BY nome_selecao")
    dados = cursor.fetchall()
    cursor.close(); conexao.close()
    return pd.DataFrame(dados)

def buscar_estadios_aux():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_estadio, nome_estadio FROM estadios ORDER BY nome_estadio")
    dados = cursor.fetchall()
    cursor.close(); conexao.close()
    return pd.DataFrame(dados)

def buscar_arbitros_aux():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_arbitro, nome_arbitro FROM arbitros ORDER BY nome_arbitro")
    dados = cursor.fetchall()
    cursor.close(); conexao.close()
    return pd.DataFrame(dados)

def listar_partidas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    # Mantido o LEFT JOIN tolerante para garantir a renderização de tudo
    cursor.execute("""
        SELECT 
            p.id_partida,
            p.data_partida,
            COALESCE(s1.nome_selecao, 'Não Mapeada') AS selecao_1,
            COALESCE(s2.nome_selecao, 'Não Mapeada') AS selecao_2,
            COALESCE(e.nome_estadio, 'Estádio Não Informado') AS nome_estadio,
            COALESCE(a.nome_arbitro, 'Árbitro Não Informado') AS nome_arbitro,
            p.quantidade_gols_selecao_1,
            p.quantidade_gols_selecao_2,
            p.vencedor
        FROM partidas p
        LEFT JOIN selecoes s1 ON p.id_selecao_1 = s1.id_selecao
        LEFT JOIN selecoes s2 ON p.id_selecao_2 = s2.id_selecao
        LEFT JOIN estadios e ON p.id_estadio = e.id_estadio
        LEFT JOIN arbitros a ON p.id_arbitro = a.id_arbitro
        ORDER BY p.data_partida DESC
    """)
    dados = cursor.fetchall()
    cursor.close(); conexao.close()
    return pd.DataFrame(dados)

def inserir_partida(data_partida, id_estadio, id_selecao_1, id_selecao_2, id_arbitro, gols1, gols2, vencedor):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO partidas
        (data_partida, id_estadio, id_selecao_1, id_selecao_2, id_arbitro, quantidade_gols_selecao_1, quantidade_gols_selecao_2, vencedor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (data_partida, id_estadio, id_selecao_1, id_selecao_2, id_arbitro, gols1, gols2, vencedor))
    conexao.commit(); cursor.close(); conexao.close()

def excluir_partida(id_partida):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM partidas WHERE id_partida = %s", (id_partida,))
    conexao.commit(); cursor.close(); conexao.close()

# ==============================================================================
# INTERFACE OPERACIONAL
# ==============================================================================

# Cabeçalho Padronizado do Módulo
st.markdown("""
<div class="dash-header">
    <div class="eyebrow">⚽ Módulo de Persistência Operacional</div>
    <h1>Partidas da Copa</h1>
    <div class="sub">Interface de gerenciamento de dados transacionais — inserção, leitura e exclusão síncrona no MySQL</div>
</div>
""", unsafe_allow_html=True)

df_partidas = listar_partidas()
df_selecoes = buscar_selecoes_aux()
df_estadios = buscar_estadios_aux()
df_arbitros = buscar_arbitros_aux()

st.markdown('<div class="section-label">Ações de Controle</div>', unsafe_allow_html=True)
aba1, aba2, aba3 = st.tabs(["📋 Visualizar Calendário", "➕ Cadastrar Partida", "🗑️ Excluir Registro"])

# ── ABA 1: VISUALIZAR CALENDÁRIO ──────────────────────────────────────────────
with aba1:
    st.markdown('<div class="operation-card">', unsafe_allow_html=True)
    st.markdown('<div class="operation-title">Tabela Geral de Confrontos</div>', unsafe_allow_html=True)
    st.markdown('<div class="operation-sub">Grade cronológica de partidas computadas no servidor relacional</div>', unsafe_allow_html=True)
    
    if df_partidas.empty:
        st.info("Nenhuma partida registrada até o momento.")
    else:
        df_exibir = df_partidas.rename(columns={
            'selecao_1': 'Seleção 1',
            'selecao_2': 'Seleção 2',
            'nome_estadio': 'Estádio Sede',
            'nome_arbitro': 'Árbitro',
            'quantidade_gols_selecao_1': 'Placar 1',
            'quantidade_gols_selecao_2': 'Placar 2',
            'data_partida': 'Data'
        })
        st.dataframe(df_exibir[['Data', 'Seleção 1', 'Placar 1', 'Placar 2', 'Seleção 2', 'Estádio Sede', 'Árbitro']], use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── ABA 2: CADASTRAR PARTIDA ──────────────────────────────────────────────────
with aba2:
    st.markdown('<div class="operation-card">', unsafe_allow_html=True)
    st.markdown('<div class="operation-title">Registrar Novo Confronto</div>', unsafe_allow_html=True)
    
    if not df_selecoes.empty and not df_estadios.empty and not df_arbitros.empty:
        selecao_dict = {s["nome_selecao"]: s["id_selecao"] for _, s in df_selecoes.iterrows()}
        estadio_dict = {e["nome_estadio"]: e["id_estadio"] for _, e in df_estadios.iterrows()}
        arbitro_dict = {a["nome_arbitro"]: a["id_arbitro"] for _, a in df_arbitros.iterrows()}
        
        col1, col2 = st.columns(2)
        with col1:
            s1 = st.selectbox("Seleção 1", list(selecao_dict.keys()), key="p_sel1")
            s2 = st.selectbox("Seleção 2", list(selecao_dict.keys()), key="p_sel2")
        with col2:
            estadio = st.selectbox("Estádio Sede", list(estadio_dict.keys()), key="p_est")
            arbitro = st.selectbox("Árbitro da Partida", list(arbitro_dict.keys()), key="p_arb")
        
        data = st.date_input("Data da Partida", key="p_data")
        
        col3, col4 = st.columns(2)
        with col3:
            g1 = st.number_input("Gols da Seleção 1", min_value=0, step=1, key="p_g1")
        with col4:
            g2 = st.number_input("Gols da Seleção 2", min_value=0, step=1, key="p_g2")
        
        if g1 > g2:
            vencedor = selecao_dict[s1]
        elif g2 > g1:
            vencedor = selecao_dict[s2]
        else:
            vencedor = None
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Salvar Partida no Banco"):
            if s1 == s2:
                st.error("Inconsistência Relacional: Uma seleção não pode jogar contra ela mesma!")
            else:
                try:
                    inserir_partida(data, estadio_dict[estadio], selecao_dict[s1], selecao_dict[s2], arbitro_dict[arbitro], g1, g2, vencedor)
                    st.success("Partida registrada com sucesso!")
                    st.rerun()
                except mysql.connector.Error as err:
                    st.error(f"Erro no banco de dados: {err.msg}")
    else:
        st.warning("Certifique-se de que existem seleções, estádios e árbitros cadastrados.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── ABA 3: EXCLUIR REGISTRO ───────────────────────────────────────────────────
with aba3:
    st.markdown('<div class="operation-card">', unsafe_allow_html=True)
    st.markdown('<div class="operation-title">Excluir Histórico de Jogos</div>', unsafe_allow_html=True)
    
    if not df_partidas.empty:
        partidas_dict = {
            f"{row['selecao_1']} {row['quantidade_gols_selecao_1']} x {row['quantidade_gols_selecao_2']} {row['selecao_2']} ({row['data_partida']})": row["id_partida"]
            for _, row in df_partidas.iterrows()
        }
        
        escolha = st.selectbox("Selecione a partida para apagar", list(partidas_dict.keys()), key="p_del")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("Excluir Registro Definitivamente"):
            excluir_partida(partidas_dict[escolha])
            st.success("Partida removida do banco de dados!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Nenhuma partida registrada disponível para exclusão.")
    st.markdown('</div>', unsafe_allow_html=True)

# SIDEBAR INSTITUCIONAL PADRONIZADO
st.sidebar.markdown("### PROJETO")
st.sidebar.markdown("**Banco de Dados I** Sistemas de Informação")
st.sidebar.markdown("---")
st.sidebar.markdown("### EQUIPE")
for autor in ["Arthur Ferreira Barbosa", "Guilherme Nery Rocha", "Isadora Morais", "Kassiane Gomes da Silva", "Leandro Augusto Barboza da Silva", "Wilka Vitória G. do Nascimento"]:
    st.sidebar.markdown(f"· {autor}")