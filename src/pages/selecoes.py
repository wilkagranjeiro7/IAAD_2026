import streamlit as st
import pandas as pd
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

    /* Botões Padrão e Perigo dentro do escopo do design do grupo */
    .stButton > button, .stForm submit_button > button {
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
# FUNÇÕES AUXILIARES DE BANCO
# ==============================================================================
def listar_grupos_aux():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_grupo, nome_grupo FROM grupos ORDER BY nome_grupo")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)

def listar_selecoes():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            s.id_selecao,
            s.nome_selecao,
            s.continente,
            s.tecnico,
            s.titulos,
            g.id_grupo,
            g.nome_grupo
        FROM selecoes s
        LEFT JOIN grupos g ON s.id_grupo = g.id_grupo
        ORDER BY g.id_grupo, s.nome_selecao
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)

def inserir_selecao(nome, continente, tecnico, titulos, id_grupo):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO selecoes (nome_selecao, continente, tecnico, titulos, id_grupo)
        VALUES (%s,%s,%s,%s,%s)
    """, (nome, continente, tecnico, titulos, id_grupo))
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_selecao(id_selecao):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM selecoes WHERE id_selecao = %s", (id_selecao,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

def atualizar_selecao(id_selecao, nome, continente, tecnico, titulos, id_grupo):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE selecoes
        SET nome_selecao=%s, continente=%s, tecnico=%s, titulos=%s, id_grupo=%s
        WHERE id_selecao=%s
    """, (nome, continente, tecnico, titulos, id_grupo, id_selecao))
    conexao.commit()
    cursor.close()
    conexao.close()

def excluir_selecao(id_selecao):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_partida FROM partidas WHERE id_selecao_1 = %s OR id_selecao_2 = %s", (id_selecao, id_selecao))
        partidas_ids = [row[0] for row in cursor.fetchall()]
        
        if partidas_ids:
            placeholders = ','.join(['%s'] * len(partidas_ids))
            cursor.execute(f"DELETE FROM gols WHERE id_partida IN ({placeholders})", partidas_ids)
            cursor.execute(f"DELETE FROM cartoes WHERE id_partida IN ({placeholders})", partidas_ids)
        
        cursor.execute("DELETE FROM partidas WHERE id_selecao_1 = %s", (id_selecao,))
        cursor.execute("DELETE FROM partidas WHERE id_selecao_2 = %s", (id_selecao,))
        
        cursor.execute("""
            DELETE g FROM gols g
            JOIN jogadores j ON g.id_jogador = j.id_jogador
            WHERE j.id_selecao = %s
        """, (id_selecao,))
        
        cursor.execute("""
            DELETE c FROM cartoes c
            JOIN jogadores j ON c.id_jogador = j.id_jogador
            WHERE j.id_selecao = %s
        """, (id_selecao,))
        
        cursor.execute("DELETE FROM jogadores WHERE id_selecao = %s", (id_selecao,))
        cursor.execute("DELETE FROM selecoes WHERE id_selecao = %s", (id_selecao,))
        
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        raise e
    finally:
        cursor.close()
        conexao.close()

# ==============================================================================
# EXECUÇÃO E RENDERIZAÇÃO DA INTERFACE
# ==============================================================================

df = listar_selecoes()
grupos_df = listar_grupos_aux()

# HEADER (Design System Unificado do Grupo)
st.markdown("""
<div class="dash-header">
    <div class="eyebrow">🏆 Federações Internacionais</div>
    <h1>Seleções</h1>
    <div class="sub">Inscrição, chaveamento e relatórios de federações nacionais registradas no campeonato</div>
</div>
""", unsafe_allow_html=True)

# Bloco de KPIs Dinâmicos Baseados no Seu Código
if not df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">🏳️</span>
            <div class="kpi-value">{len(df)}</div>
            <div class="kpi-label">Seleções Inscritas</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">🌍</span>
            <div class="kpi-value">{df["continente"].nunique()}</div>
            <div class="kpi-label">Continentes Distintos</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        campea = df.loc[df["titulos"].idxmax()] if df["titulos"].max() > 0 else None
        titulo_val = f"{campea['nome_selecao']} ({campea['titulos']}🏆)" if campea is not None else "Nenhum"
        st.markdown(f"""
        <div class="kpi-card">
            <span class="kpi-icon">⭐</span>
            <div class="kpi-value" style="font-size:1.4rem; padding-top:4px">{titulo_val}</div>
            <div class="kpi-label">Maior Detentora de Títulos</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ABAS DO CRUD
st.markdown('<div class="section-label">Gerenciamento</div>', unsafe_allow_html=True)
aba_lista, aba_cadastrar, aba_editar = st.tabs(["📋 Lista & Filtros", "➕ Cadastrar Seleção", "🔧 Editar Seleção"])

# ── ABA 1: LISTAR E FILTRAR SELEÇÕES ──────────────────────────────────────────
with aba_lista:
    if not df.empty:
        # Filtros no Design System Light do Grupo
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-card-title">🔍 Filtragem Avançada da Amostra</div>', unsafe_allow_html=True)
        col_busca, col_cont, col_grp = st.columns([2, 1, 1])
        with col_busca:
            busca = st.text_input("Buscar pelo nome do país:", placeholder="Digite o país...")
        with col_cont:
            continentes_opcoes = ["Todos"] + sorted(df["continente"].unique().tolist())
            filtro_continente = st.selectbox("Filtrar por Continente:", continentes_opcoes)
        with col_grp:
            grupos_opcoes = ["Todos"] + sorted(grupos_df["nome_grupo"].unique().tolist()) if not grupos_df.empty else ["Todos"]
            filtro_grupo = st.selectbox("Filtrar por Grupo Chave:", grupos_opcoes)
        st.markdown('</div>', unsafe_allow_html=True)

        # Processamento de Filtros no DataFrame
        df_filtrado = df.copy()
        if busca:
            df_filtrado = df_filtrado[df_filtrado["nome_selecao"].str.contains(busca, case=False)]
        if filtro_continente != "Todos":
            df_filtrado = df_filtrado[df_filtrado["continente"] == filtro_continente]
        if filtro_grupo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["nome_grupo"] == filtro_grupo]

        # Renderização do Grid por Grupos
        if df_filtrado.empty:
            st.warning("⚠️ Nenhuma federação atende aos filtros definidos acima.")
        else:
            st.markdown('<div class="table-card">', unsafe_allow_html=True)
            for grupo in sorted(df_filtrado["nome_grupo"].dropna().unique()):
                df_grupo = df_filtrado[df_filtrado["nome_grupo"] == grupo]
                
                st.markdown(f"<div style='font-size:0.9rem; font-weight:700; color:#1A73E8; margin-bottom:12px;'>🏆 GRUPO {grupo}</div>", unsafe_allow_html=True)
                
                # Grid customizado adaptado ao padrão
                for _, selecao in df_grupo.iterrows():
                    cols = st.columns([2.5, 1.5, 2, 2, 1])
                    with cols[0]:
                        st.markdown(f"<span style='color:#1A1F2E; font-weight:600;'>{selecao['nome_selecao']}</span>", unsafe_allow_html=True)
                    with cols[1]:
                        st.caption(f"🌍 {selecao['continente']}")
                    with cols[2]:
                        st.markdown(f"<span style='font-size:0.9rem; color:#555F6D;'>👔 {selecao['tecnico']}</span>", unsafe_allow_html=True)
                    with cols[3]:
                        st.markdown(f"<span style='font-size:0.9rem; color:#555F6D;'>⭐ {selecao['titulos']} título(s)</span>", unsafe_allow_html=True)
                    with cols[4]:
                        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
                        if st.button("Excluir", key=f"del_{selecao['id_selecao']}", use_container_width=True):
                            excluir_selecao(selecao['id_selecao'])
                            st.success(f"{selecao['nome_selecao']} removida!")
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("<div style='border-top:1px solid #F3F4F6; margin:8px 0;'></div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nenhuma seleção cadastrada no banco de dados.")

# ── ABA 2: CADASTRAR NOVA SELEÇÃO ─────────────────────────────────────────────
with aba_cadastrar:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">➕ Registrar Nova Seleção Nacional</div>', unsafe_allow_html=True)
    
    if not grupos_df.empty:
        opcoes_grupo = {row["nome_grupo"]: row["id_grupo"] for _, row in grupos_df.iterrows()}
        
        col1, col2 = st.columns(2)
        with col1:
            nome_cad = st.text_input("Nome da Seleção (País)", max_chars=50, placeholder="Ex: Brasil")
            continente_cad = st.selectbox("Continente de Origem", ["America", "Europa", "Africa", "Ásia", "Oceania"], key="cad_cont")
            tecnico_cad = st.text_input("Nome do Diretor Técnico", max_chars=50, placeholder="Ex: Carlo Ancelotti")
        with col2:
            titulos_cad = st.number_input("Quantidade de Títulos Mundiais", min_value=0, step=1, key="cad_tit")
            grupo_nome_cad = st.selectbox("Vincular ao Grupo da Copa", list(opcoes_grupo.keys()), key="cad_grp")
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Inscrever Seleção no Torneio", key="btn_cad_selecao"):
            if nome_cad.strip():
                inserir_selecao(nome_cad.strip(), continente_cad, tecnico_cad, titulos_cad, opcoes_grupo[grupo_nome_cad])
                st.success(f"✅ Seleção {nome_cad} cadastrada com sucesso!")
                st.rerun()
            else:
                st.error("Erro de preenchimento: O nome da seleção/país é obrigatório!")
    else:
        st.warning("Ação bloqueada: Cadastre ao menos um grupo-chave antes de instanciar novas seleções.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── ABA 3: EDITAR SELEÇÃO EXISTENTE ───────────────────────────────────────────
with aba_editar:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-card-title">🔧 Atualizar Metadados de Federação</div>', unsafe_allow_html=True)
    
    if not df.empty and not grupos_df.empty:
        opcoes_selecao = {row["nome_selecao"]: row["id_selecao"] for _, row in df.iterrows()}
        selecao_escolhida = st.selectbox("Selecione o país para retificação de dados:", list(opcoes_selecao.keys()), key="sel_edit_combo")
        
        # Carregamento estável dos dados vigentes
        registro = buscar_selecao(opcoes_selecao[selecao_escolhida])
        opcoes_grupo = {row["nome_grupo"]: row["id_grupo"] for _, row in grupos_df.iterrows()}
        
        continentes_lista = ["America", "Europa", "Africa", "Ásia", "Oceania"]
        idx_cont = continentes_lista.index(registro["continente"]) if registro["continente"] in continentes_lista else 0
        
        nome_grp_atual = [k for k, v in opcoes_grupo.items() if v == registro["id_grupo"]]
        idx_grp = list(opcoes_grupo.keys()).index(nome_grp_atual[0]) if nome_grp_atual else 0

        col1, col2 = st.columns(2)
        with col1:
            nome_edit = st.text_input("Nome da Federação", value=registro["nome_selecao"], max_chars=50)
            continente_edit = st.selectbox("Continente Sede", continentes_lista, index=idx_cont, key="edit_cont_box")
            tecnico_edit = st.text_input("Técnico Atual", value=registro["tecnico"], max_chars=50)
        with col2:
            titulos_edit = st.number_input("Títulos Conquistados", value=int(registro["titulos"]), min_value=0, step=1, key="edit_tit_box")
            grupo_nome_edit = st.selectbox("Chaveamento de Grupo", list(opcoes_grupo.keys()), index=idx_grp, key="edit_grp_box")
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Salvar Modificações no Registro", key="btn_update_selecao"):
            if nome_edit.strip():
                atualizar_selecao(registro["id_selecao"], nome_edit.strip(), continente_edit, tecnico_edit, titulos_edit, opcoes_grupo[grupo_nome_edit])
                st.success(f"✅ Histórico de {nome_edit} atualizado com sucesso!")
                st.rerun()
            else:
                st.error("Erro de validação: O nome da seleção/país não pode ficar em branco.")
    else:
        st.warning("Operação indisponível: Dados insuficientes carregados no banco de dados para edição.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR INSTITUCIONAL PADRONIZADO
# ==============================================================================
st.sidebar.markdown("### PROJETO")
st.sidebar.markdown("""
**Banco de Dados I** Sistemas de Informação
""")
st.sidebar.markdown("---")
st.sidebar.markdown("### EQUIPE")
autores = [
    "Arthur Ferreira Barbosa",
    "Guilherme Nery Rocha",
    "Isadora Morais",
    "Kassiane Gomes da Silva",
    "Leandro Augusto Barboza da Silva",
    "Wilka Vitória G. do Nascimento",
]
for a in autores:
    st.sidebar.markdown(f"· {a}")