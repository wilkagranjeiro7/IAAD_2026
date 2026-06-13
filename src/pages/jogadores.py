import streamlit as st
import pandas as pd
import mysql.connector  # Adicionado para capturar o erro da Trigger
from conexao import conectar

st.set_page_config(
    page_title="Copa do Mundo 2026 · Dashboard Estatístico",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# SISTEMA DE DESIGN — MESMO PADRÃO DO DASHBOARD (LIGHT)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700;900&display=swap');

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
    [data-testid="stSidebar"] h3 {
        color: #1A1F2E !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Header */
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

    /* KPI cards */
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
    .kpi-card .kpi-icon {
        font-size: 1.6rem;
        margin-bottom: 10px;
        display: block;
    }
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

    /* Seção */
    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #1A73E8;
        margin-bottom: 6px;
    }

    /* Cards Operacionais do CRUD */
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
        margin: 30px 0;
    }

    /* Inputs Customizados */
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
    .stSelectbox > div > div {
        border: 1px solid #D1D5DB !important; border-radius: 6px !important;
        font-size: 0.95rem !important;
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
# FUNÇÕES DE CONSULTA DO BANCO DE DADOS
# ==============================================================================

POSICOES = [
    "Goleiro", "Zagueiro", "Lateral Direito", "Lateral Esquerdo",
    "Volante", "Meio Campo", "Atacante", "Centroavante",
    "Ponta Direita", "Ponta Esquerda"
]

def listar_selecoes_combo():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_selecao, nome_selecao FROM selecoes ORDER BY nome_selecao")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados

def listar_jogadores():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT j.id_jogador, j.nome_jogador, j.posicao, j.numero_camisa,
               j.data_nascimento, s.nome_selecao
        FROM jogadores j
        JOIN selecoes s ON j.id_selecao = s.id_selecao
        ORDER BY s.nome_selecao, j.numero_camisa
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)

def inserir_jogador(nome, posicao, camisa, nascimento, id_selecao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO jogadores (nome_jogador, posicao, numero_camisa, data_nascimento, id_selecao)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, posicao, camisa, nascimento, id_selecao))
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_jogador(id_jogador):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jogadores WHERE id_jogador = %s", (id_jogador,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

def atualizar_jogador(id_jogador, nome, posicao, camisa, nascimento, id_selecao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE jogadores
        SET nome_jogador=%s, posicao=%s, numero_camisa=%s, data_nascimento=%s, id_selecao=%s
        WHERE id_jogador=%s
    """, (nome, posicao, camisa, nascimento, id_selecao, id_jogador))
    conexao.commit()
    cursor.close()
    conexao.close()

def excluir_jogador(id_jogador):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM jogadores WHERE id_jogador = %s", (id_jogador,))
    conexao.commit()
    cursor.close()
    conexao.close()

# ==============================================================================
# EXECUÇÃO E RENDERIZAÇÃO DA INTERFACE
# ==============================================================================

df = listar_jogadores()
selecoes_disponiveis = listar_selecoes_combo()

# Cálculos dinâmicos para alimentação das Métricas
total_jogadores  = len(df)
total_selecoes   = df["nome_selecao"].nunique() if not df.empty else 0
posicao_mais_com = df["posicao"].value_counts().idxmax() if not df.empty else "—"

# HEADER (Design System Light)
st.markdown("""
<div class="dash-header">
    <div class="eyebrow">⚽ Análise de Elencos Registrados</div>
    <h1>Jogadores</h1>
    <div class="sub">Módulo transacional para gerenciamento, triagem e controle de atletas cadastrados no torneio</div>
</div>
""", unsafe_allow_html=True)

# Bloco Superior de KPIs
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">👤</span>
        <div class="kpi-value">{total_jogadores}</div>
        <div class="kpi-label">Jogadores cadastrados</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🌍</span>
        <div class="kpi-value">{total_selecoes}</div>
        <div class="kpi-label">Seleções representadas</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">📌</span>
        <div class="kpi-value" style="font-size:1.3rem; padding-top:4px">{posicao_mais_com}</div>
        <div class="kpi-label">Posição predominante</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Abas Operacionais para as Ações do CRUD
st.markdown('<div class="section-label">Ações de Controle</div>', unsafe_allow_html=True)
aba1, aba2, aba3 = st.tabs(["➕ Cadastrar Atleta", "✏️ Editar Registro", "🗑️ Excluir Registro"])

# ── CADASTRAR JOGADOR (INSERÇÃO COM TRATAMENTO DA TRIGGER) ────────────────────
with aba1:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">➕ Inserir Novo Jogador</div>', unsafe_allow_html=True)

    if selecoes_disponiveis:
        col1, col2 = st.columns(2)
        with col1:
            nome      = st.text_input("Nome Completo", key="j_nome", placeholder="Ex: Vinicius Jr.")
            posicao   = st.selectbox("Posição de Ofício", POSICOES, key="j_posicao")
            camisa    = st.number_input("Número do Uniforme", min_value=1, max_value=99, key="j_camisa")
        with col2:
            nascimento = st.date_input("Data de Nascimento", key="j_nascimento")
            opcoes_sel = {s["nome_selecao"]: s["id_selecao"] for s in selecoes_disponiveis}
            selecao    = st.selectbox("Seleção Correspondente", list(opcoes_sel.keys()), key="j_selecao")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Cadastrar Jogador no Banco", key="btn_cad_jogador"):
            if nome.strip():
                try:
                    # Tenta realizar a query de inserção normal
                    inserir_jogador(nome.strip(), posicao, camisa, nascimento, opcoes_sel[selecao])
                    st.success("✅ Jogador cadastrado com sucesso!")
                    st.rerun()
                except mysql.connector.Error as err:
                    # Captura o erro customizado gerado pela Trigger se o atleta for menor de 18 anos
                    st.error(f"❌ {err.msg}")
            else:
                st.error("Inconsistência de campo: Digite o nome do jogador antes de salvar.")
    else:
        st.warning("Ação bloqueada: Registre ao menos uma federação na tabela 'selecoes' antes de adicionar atletas.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── EDITAR JOGADOR (ATUALIZAÇÃO DE REGISTROS) ─────────────────────────────────
with aba2:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">✏️ Modificar Metadados do Atleta</div>', unsafe_allow_html=True)

    if not df.empty and selecoes_disponiveis:
        opcoes_jog     = {f"{l['nome_jogador']} ({l['nome_selecao']})": l["id_jogador"] for _, l in df.iterrows()}
        jog_escolhido  = st.selectbox("Selecione o jogador alvo", list(opcoes_jog.keys()), key="editar_jogador")
        registro       = buscar_jogador(opcoes_jog[jog_escolhido])

        col1, col2 = st.columns(2)
        with col1:
            nome_edit      = st.text_input("Nome Retificado", value=registro["nome_jogador"], key="edit_nome_jogador")
            posicao_edit   = st.selectbox("Posição Retificada", POSICOES, index=POSICOES.index(registro["posicao"]) if registro["posicao"] in POSICOES else 0, key="edit_posicao_jogador")
            camisa_edit    = st.number_input("Número Retificado", min_value=1, max_value=99, value=int(registro["numero_camisa"]), key="edit_camisa")
        with col2:
            nascimento_edit = st.date_input("Nascimento Retificado", value=registro["data_nascimento"], key="edit_nascimento")
            opcoes_sel      = {s["nome_selecao"]: s["id_selecao"] for s in selecoes_disponiveis}
            nome_sel_atual  = [k for k, v in opcoes_sel.items() if v == registro["id_selecao"]]
            index_sel       = list(opcoes_sel.keys()).index(nome_sel_atual[0]) if nome_sel_atual else 0
            selecao_edit    = st.selectbox("Seleção Retificada", list(opcoes_sel.keys()), index=index_sel, key="edit_selecao")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Salvar Modificações", key="btn_update_jogador"):
            try:
                atualizar_jogador(registro["id_jogador"], nome_edit, posicao_edit, camisa_edit, nascimento_edit, opcoes_sel[selecao_edit])
                st.success("✅ Histórico do jogador atualizado com sucesso!")
                st.rerun()
            except mysql.connector.Error as err:
                st.error(f"❌ {err.msg}")
    else:
        st.warning("Operação indisponível: Nenhuma entidade localizada para alteração estrutural.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── EXCLUIR JOGADOR (REMOÇÃO PERIGOSA COM BOTÃO VERMELHO) ─────────────────────
with aba3:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">🗑️ Exclusão Definitiva de Registro</div>', unsafe_allow_html=True)

    if not df.empty:
        opcoes_jog = {f"{l['nome_jogador']} ({l['nome_selecao']})": l["id_jogador"] for _, l in df.iterrows()}
        jog_del    = st.selectbox("Selecione o registro para exclusão", list(opcoes_jog.keys()), key="excluir_jogador")
        st.warning(f"Atenção: A remoção de **{jog_del}** expurgará permanentemente o registro no banco.")
        
        # Injeção da classe CSS vermelha de perigo para o botão de exclusão
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("Confirmar Exclusão Permanente", key="btn_delete_jogador"):
            excluir_jogador(opcoes_jog[jog_del])
            st.success("✅ Jogador removido com sucesso!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Operação indisponível: Tabela 'jogadores' vazia.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# VISUALIZAÇÃO GERAL EM DATAFRAME INTEGRADO
st.markdown('<div class="section-label">Registros Armazenados</div>', unsafe_allow_html=True)
st.markdown('<div class="table-card">', unsafe_allow_html=True)
st.markdown('<div class="table-title">📋 Lista Completa de Atletas Homologados</div>', unsafe_allow_html=True)

if df.empty:
    st.info("Nenhum atleta mapeado no momento.")
else:
    df_exibicao = df.rename(columns={
        "id_jogador":      "ID Interno",
        "nome_jogador":    "Nome do Atleta",
        "posicao":         "Posição de Atuação",
        "numero_camisa":   "Nº da Camisa",
        "data_nascimento": "Data de Nascimento",
        "nome_selecao":    "Federação / Seleção"
    })
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)

# BARRA LATERAL INSTITUCIONAL
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