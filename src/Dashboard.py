import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from conexao import conectar

st.set_page_config(
    page_title="Copa do Mundo 2026 · Dashboard Estatístico",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# SISTEMA DE DESIGN — PALETA BRANCA / LIGHT
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
    .chart-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1A1F2E;
        margin-bottom: 2px;
    }
    .chart-sub {
        font-size: 0.82rem;
        color: #6B7280;
        margin-bottom: 12px;
    }
    .chart-wrap {
        background: #FFFFFF;
        border: 1px solid #E2E6EA;
        border-radius: 10px;
        padding: 20px 18px 10px 18px;
        margin-bottom: 18px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }

    /* Tabelas */
    .table-card {
        background: #FFFFFF;
        border: 1px solid #E2E6EA;
        border-radius: 10px;
        padding: 20px;
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
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES DE CONSULTA
# ==============================================================================

def contar_selecoes():
    conn = conectar(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM selecoes")
    r = cur.fetchone()[0]; cur.close(); conn.close(); return r

def contar_jogadores():
    conn = conectar(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM jogadores")
    r = cur.fetchone()[0]; cur.close(); conn.close(); return r

def contar_partidas():
    conn = conectar(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM partidas")
    r = cur.fetchone()[0]; cur.close(); conn.close(); return r

def contar_gols():
    conn = conectar(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM gols")
    r = cur.fetchone()[0]; cur.close(); conn.close()
    return int(r) if r else 0

def selecoes_por_continente():
    conn = conectar(); cur = conn.cursor()
    cur.execute("SELECT continente, COUNT(*) as total FROM selecoes GROUP BY continente ORDER BY total DESC")
    d = cur.fetchall(); cur.close(); conn.close()
    return pd.DataFrame(d, columns=["Continente", "Total"])

def top_campeas():
    conn = conectar(); cur = conn.cursor()
    cur.execute("SELECT nome_selecao, titulos FROM selecoes WHERE titulos > 0 ORDER BY titulos DESC LIMIT 5")
    d = cur.fetchall(); cur.close(); conn.close()
    return pd.DataFrame(d, columns=["Seleção", "Títulos"])

def defesa_menos_vazada():
    conn = conectar(); cur = conn.cursor(dictionary=True)
    # CORRIGIDO: O ORDER BY agora usa a mesma fórmula do SUM/CASE em vez do alias com espaço e crase
    cur.execute("""
        SELECT s.nome_selecao as `Seleção`,
            COALESCE(SUM(CASE
                WHEN p.id_selecao_1 = s.id_selecao THEN p.quantidade_gols_selecao_2
                WHEN p.id_selecao_2 = s.id_selecao THEN p.quantidade_gols_selecao_1
                ELSE 0 END), 0) as `Gols Sofridos`
        FROM selecoes s
        LEFT JOIN partidas p ON (p.id_selecao_1 = s.id_selecao OR p.id_selecao_2 = s.id_selecao)
        GROUP BY s.id_selecao, s.nome_selecao
        ORDER BY COALESCE(SUM(CASE
                WHEN p.id_selecao_1 = s.id_selecao THEN p.quantidade_gols_selecao_2
                WHEN p.id_selecao_2 = s.id_selecao THEN p.quantidade_gols_selecao_1
                ELSE 0 END), 0) ASC LIMIT 5
    """)
    d = cur.fetchall(); cur.close(); conn.close()
    return pd.DataFrame(d)

def selecao_mais_gols():
    conn = conectar(); cur = conn.cursor(dictionary=True)
    # CORRIGIDO: O ORDER BY usa a fórmula de soma diretamente, sem aspas ou crases
    cur.execute("""
        SELECT s.nome_selecao as `Seleção`,
            COALESCE(SUM(CASE
                WHEN p.id_selecao_1 = s.id_selecao THEN p.quantidade_gols_selecao_1
                WHEN p.id_selecao_2 = s.id_selecao THEN p.quantidade_gols_selecao_2
                ELSE 0 END), 0) as `Gols Marcados`
        FROM selecoes s
        LEFT JOIN partidas p ON (p.id_selecao_1 = s.id_selecao OR p.id_selecao_2 = s.id_selecao)
        GROUP BY s.id_selecao, s.nome_selecao
        ORDER BY COALESCE(SUM(CASE
                WHEN p.id_selecao_1 = s.id_selecao THEN p.quantidade_gols_selecao_1
                WHEN p.id_selecao_2 = s.id_selecao THEN p.quantidade_gols_selecao_2
                ELSE 0 END), 0) DESC LIMIT 5
    """)
    d = cur.fetchall(); cur.close(); conn.close()
    return pd.DataFrame(d)

def artilheiro_copa():
    conn = conectar(); cur = conn.cursor(dictionary=True)
    # CORRIGIDO: O ORDER BY agora ordena diretamente pela função agregada COUNT(g.id_gol)
    cur.execute("""
        SELECT j.nome_jogador as `Jogador`, s.nome_selecao as `Seleção`, COUNT(g.id_gol) as `Gols`
        FROM gols g
        JOIN jogadores j ON g.id_jogador = j.id_jogador
        JOIN selecoes s ON j.id_selecao = s.id_selecao
        GROUP BY j.id_jogador, j.nome_jogador, s.nome_selecao
        ORDER BY COUNT(g.id_gol) DESC LIMIT 5
    """)
    d = cur.fetchall(); cur.close(); conn.close()
    return pd.DataFrame(d)

def fair_play():
    conn = conectar(); cur = conn.cursor(dictionary=True)
    # CORRIGIDO: O ORDER BY realiza o cálculo matemático dos cartões diretamente para ordenar
    cur.execute("""
        SELECT s.nome_selecao as `Seleção`,
            COALESCE(SUM(CASE WHEN c.tipo_cartao = 'Amarelo' THEN 1 ELSE 0 END), 0) as `Amarelos`,
            COALESCE(SUM(CASE WHEN c.tipo_cartao = 'Vermelho' THEN 1 ELSE 0 END), 0) as `Vermelhos`,
            COALESCE(
                (SUM(CASE WHEN c.tipo_cartao = 'Amarelo' THEN 1 ELSE 0 END) * 1) +
                (SUM(CASE WHEN c.tipo_cartao = 'Vermelho' THEN 1 ELSE 0 END) * 3), 0
            ) as `Pontuação`
        FROM selecoes s
        LEFT JOIN jogadores j ON j.id_selecao = s.id_selecao
        LEFT JOIN cartoes c ON c.id_jogador = j.id_jogador
        GROUP BY s.id_selecao, s.nome_selecao
        ORDER BY COALESCE(
                (SUM(CASE WHEN c.tipo_cartao = 'Amarelo' THEN 1 ELSE 0 END) * 1) +
                (SUM(CASE WHEN c.tipo_cartao = 'Vermelho' THEN 1 ELSE 0 END) * 3), 0
            ) ASC LIMIT 5
    """)
    d = cur.fetchall(); cur.close(); conn.close()
    return pd.DataFrame(d)

# ==============================================================================
# CONFIGURAÇÃO PLOTLY — TEMA BRANCO
# ==============================================================================
PLOT_BG      = "#FFFFFF"
PAPER_BG     = "#FFFFFF"
GRID_COLOR   = "#F0F2F5"
TICK_COLOR   = "#6B7280"
FONT_COLOR   = "#1A1F2E"
BLUE_MAIN    = "#1A73E8"
AMBER_MAIN   = "#F59E0B"

LAYOUT_BASE = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=PLOT_BG,
    font=dict(family="Inter, sans-serif", color=FONT_COLOR, size=13),
    margin=dict(t=10, b=10, l=10, r=10),
    height=250,
    showlegend=False,
)

AXIS_STYLE = dict(
    showgrid=True,
    gridcolor=GRID_COLOR,
    tickcolor=TICK_COLOR,
    tickfont=dict(color=TICK_COLOR, size=12),
    linecolor="#E2E6EA",
    zeroline=False,
)

# ==============================================================================
# INTERFACE
# ==============================================================================

st.markdown("""
<div class="dash-header">
    <div class="eyebrow">⚽ Análise Estatística Computacional</div>
    <h1>Copa do Mundo 2026</h1>
    <div class="sub">Indicadores gerados a partir do banco de dados relacional MySQL — atualização em tempo real</div>
</div>
""", unsafe_allow_html=True)

try:
    # ── KPIs ──────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpi_data = [
        ("🌍", contar_selecoes(),   "Seleções"),
        ("👤", contar_jogadores(),  "Jogadores"),
        ("📋", contar_partidas(),   "Partidas"),
        ("⚽", contar_gols(),       "Gols no torneio"),
    ]
    for col, (icon, val, label) in zip([k1, k2, k3, k4], kpi_data):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <span class="kpi-icon">{icon}</span>
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── GRÁFICOS ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Distribuição &amp; Desempenho</div>', unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2, gap="medium")

    with col_g1:
        # Fig 1 — Continentes
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Seleções por continente</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Distribuição absoluta das federações participantes</div>', unsafe_allow_html=True)
        df_cont = selecoes_por_continente()
        if not df_cont.empty:
            fig = go.Figure(go.Bar(
                x=df_cont["Continente"],
                y=df_cont["Total"],
                text=df_cont["Total"],
                textposition="inside",
                textfont=dict(color="#FFFFFF", size=14, family="Inter"),
                marker=dict(
                    color=df_cont["Total"],
                    colorscale=[[0, "#93C5FD"], [1, "#1A73E8"]],
                    showscale=False,
                    line=dict(width=0),
                )
            ))
            fig.update_layout(**LAYOUT_BASE)
            fig.update_xaxes(**AXIS_STYLE, title=None)
            fig.update_yaxes(**AXIS_STYLE, title=None, range=[0, None])
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Fig 2 — Gols marcados
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Potência ofensiva — Top 5 seleções</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Gols marcados por federação no torneio</div>', unsafe_allow_html=True)
        df_gm = selecao_mais_gols()
        if not df_gm.empty:
            fig = go.Figure(go.Bar(
                x=df_gm["Gols Marcados"],
                y=df_gm["Seleção"],
                orientation="h",
                text=df_gm["Gols Marcados"],
                textposition="inside",
                textfont=dict(color="#FFFFFF", size=13, family="Inter"),
                marker=dict(
                    color=df_gm["Gols Marcados"],
                    colorscale=[[0, "#93C5FD"], [1, "#1A73E8"]],
                    showscale=False,
                    line=dict(width=0),
                )
            ))
            fig.update_layout(**LAYOUT_BASE, yaxis=dict(categoryorder="total ascending"))
            fig.update_xaxes(**AXIS_STYLE, title=None, range=[0, None])
            fig.update_yaxes(**AXIS_STYLE, title=None)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g2:
        # Fig 3 — Títulos
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"> Histórico de Conquistas — As 5 Maiores Campeãs</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Total de títulos mundiais acumulados</div>', unsafe_allow_html=True)
        df_camp = top_campeas()
        if not df_camp.empty:
            fig = go.Figure(go.Bar(
                x=df_camp["Títulos"],
                y=df_camp["Seleção"],
                orientation="h",
                text=df_camp["Títulos"],
                textposition="inside",
                textfont=dict(color="#FFFFFF", size=13, family="Inter"),
                marker=dict(
                    color=df_camp["Títulos"],
                    colorscale=[[0, "#FCD34D"], [1, "#D97706"]],
                    showscale=False,
                    line=dict(width=0),
                )
            ))
            fig.update_layout(**LAYOUT_BASE, yaxis=dict(categoryorder="total ascending"))
            fig.update_xaxes(**AXIS_STYLE, title=None, range=[0, None])
            fig.update_yaxes(**AXIS_STYLE, title=None)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Fig 4 — Defesa
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Solidez defensiva — Top 5</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Menor número de gols sofridos no torneio</div>', unsafe_allow_html=True)
        df_def = defesa_menos_vazada()
        if not df_def.empty:
            fig = go.Figure(go.Bar(
                x=df_def["Gols Sofridos"],
                y=df_def["Seleção"],
                orientation="h",
                text=df_def["Gols Sofridos"],
                textposition="inside",
                textfont=dict(color="#FFFFFF", size=13, family="Inter"),
                marker=dict(
                    color=df_def["Gols Sofridos"],
                    colorscale=[[0, "#6EE7B7"], [1, "#EF4444"]],
                    showscale=False,
                    line=dict(width=0),
                )
            ))
            fig.update_layout(**LAYOUT_BASE, yaxis=dict(categoryorder="total descending"))
            fig.update_xaxes(**AXIS_STYLE, title=None, range=[0, None])
            fig.update_yaxes(**AXIS_STYLE, title=None)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── TABELAS ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Rankings detalhados</div>', unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2, gap="medium")

    with col_t1:
        st.markdown('<div class="table-card"><div class="table-title">⚽ Artilharia — Top 5 goleadores</div>', unsafe_allow_html=True)
        df_art = artilheiro_copa()
        if df_art.empty:
            st.info("Aguardando início das partidas.")
        else:
            st.dataframe(df_art, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="table-card"><div class="table-title">🟨 Fair Play — Penalidades acumuladas</div>', unsafe_allow_html=True)
        df_fp = fair_play()
        if df_fp.empty:
            st.info("Nenhum cartão registrado.")
        else:
            st.dataframe(df_fp, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")

# SIDEBAR
st.sidebar.markdown("### PROJETO")
st.sidebar.markdown("""
**Banco de Dados I**  
Sistemas de Informação
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