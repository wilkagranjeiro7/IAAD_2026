import streamlit as st
from IAAD_2026.src.pages.selecoes import tela_selecoes, tela_cadastro_selecao, tela_editar_selecao
from IAAD_2026.src.pages.jogadores import tela_jogadores
from IAAD_2026.src.pages.estadios import tela_estadios
from IAAD_2026.src.pages.arbitros import tela_arbitros
from IAAD_2026.src.pages.partidas import tela_partidas
from IAAD_2026.src.pages.grupos import tela_grupos
from IAAD_2026.src.Dashboard import (
    contar_selecoes, contar_jogadores, contar_partidas, contar_gols,
    selecoes_por_continente, top_campeas, defesa_menos_vazada,
    selecao_mais_gols, artilheiro_copa, fair_play
)
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Copa do Mundo 2026", page_icon="⚽", layout="wide")

# Esconder sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Inicializar sessão
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

# ============================================
# TELA HOME (DASHBOARD)
# ============================================
def tela_home():
    
    st.title("Copa do Mundo 2026")
    st.markdown("Tabela da Copa do Mundo")
    st.markdown("---")
    
    st.header("Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Seleções", contar_selecoes())
    with col2:
        st.metric("Jogadores", contar_jogadores())
    with col3:
        st.metric("Partidas", contar_partidas())
    with col4:
        st.metric("Gols", contar_gols())
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    # Gráfico 1: Seleções por Continente (barras na vertical)
    with col1:
        st.subheader("Seleções por Continente")
        dados_cont = selecoes_por_continente()
        if dados_cont:
            df_cont = pd.DataFrame(dados_cont, columns=["continente", "total"])
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            ax1.bar(df_cont["continente"], df_cont["total"], color='gray', edgecolor='black')
            ax1.set_xlabel("Continente")
            ax1.set_ylabel("Quantidade")
            ax1.set_title("Seleções por Continente", fontsize=12)
            ax1.grid(True, linestyle='--', alpha=0.6)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig1)
        else:
            st.info("Nenhum dado disponível")
    
    # Gráfico 2: Seleções com mais títulos (barras na vertical)
    with col2:
        st.subheader("Seleções com mais Títulos")
        dados_tit = top_campeas()
        if dados_tit:
            df_tit = pd.DataFrame(dados_tit, columns=["selecao", "titulos"])
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            ax2.bar(df_tit["selecao"], df_tit["titulos"], color='gray', edgecolor='black')
            ax2.set_xlabel("Seleção")
            ax2.set_ylabel("Títulos")
            ax2.set_title("Seleções com mais Títulos", fontsize=12)
            ax2.grid(True, linestyle='--', alpha=0.6)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig2)
        else:
            st.info("Nenhum dado disponível")
    
    st.divider()
    
    # Cards de navegação
    st.subheader("Módulos do Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Seleções", use_container_width=True):
            st.session_state.pagina = "Selecoes"
            st.rerun()
        st.caption("Cadastrar e gerenciar")
    
    with col2:
        if st.button("Jogadores", use_container_width=True):
            st.session_state.pagina = "Jogadores"
            st.rerun()
        st.caption("Convocados por seleção")
    
    with col3:
        if st.button("Estádios", use_container_width=True):
            st.session_state.pagina = "Estadios"
            st.rerun()
        st.caption("Sedas da Copa")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Árbitros", use_container_width=True):
            st.session_state.pagina = "Arbitros"
            st.rerun()
        st.caption("Equipe de arbitragem")
    
    with col2:
        if st.button("Partidas", use_container_width=True):
            st.session_state.pagina = "Partidas"
            st.rerun()
        st.caption("Jogos e resultados")
    
    with col3:
        if st.button("Grupos", use_container_width=True):
            st.session_state.pagina = "Grupos"
            st.rerun()
        st.caption("A a L")


# ============================================
# ROTEADOR PRINCIPAL
# ============================================
if st.session_state.pagina == "Home":
    tela_home()
elif st.session_state.pagina == "Selecoes":
    tela_selecoes()
elif st.session_state.pagina == "CadastroSelecao":
    tela_cadastro_selecao()
elif st.session_state.pagina == "EditarSelecao":
    tela_editar_selecao()
elif st.session_state.pagina == "Jogadores":
    tela_jogadores()
elif st.session_state.pagina == "Estadios":
    tela_estadios()
elif st.session_state.pagina == "Arbitros":
    tela_arbitros()
elif st.session_state.pagina == "Partidas":
    tela_partidas()
elif st.session_state.pagina == "Grupos":
    tela_grupos()