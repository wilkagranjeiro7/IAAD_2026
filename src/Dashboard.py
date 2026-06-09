import streamlit as st
import pandas as pd
from conexao import conectar 

# ==============================================================================
# FUNÇÕES DE CONSULTA ANALÍTICA (MÉTODOS DO SEU AMIGO)
# ==============================================================================

def contar_selecoes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM selecoes")
    total = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    return total

def contar_jogadores():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM jogadores")
    total = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    return total

def contar_partidas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM partidas")
    total = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    return total

def contar_gols():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT SUM(quantidade_gols_selecao_1) + SUM(quantidade_gols_selecao_2) FROM partidas")
    resultado = cursor.fetchone()[0]
    total = int(resultado) if resultado else 0
    cursor.close()
    conexao.close()
    return total

def selecoes_por_continente():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT continente, COUNT(*) as total 
        FROM selecoes 
        GROUP BY continente 
        ORDER BY total DESC
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados, columns=["Continente", "Total"])

def top_campeas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT nome_selecao, titulos 
        FROM selecoes 
        WHERE titulos > 0 
        ORDER BY titulos DESC 
        LIMIT 5
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados, columns=["Seleção", "Títulos"])

def defesa_menos_vazada():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            s.nome_selecao as "Seleção",
            COALESCE(SUM(CASE 
                WHEN p.id_selecao_1 = s.id_selecao THEN p.quantidade_gols_selecao_2
                WHEN p.id_selecao_2 = s.id_selecao THEN p.quantidade_gols_selecao_1
                ELSE 0
            END), 0) as "Gols Sofridos"
        FROM selecoes s
        LEFT JOIN partidas p ON (p.id_selecao_1 = s.id_selecao OR p.id_selecao_2 = s.id_selecao)
        GROUP BY s.id_selecao
        ORDER BY "Gols Sofridos" ASC
        LIMIT 5
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)

def selecao_mais_gols():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            s.nome_selecao as "Seleção",
            COALESCE(SUM(CASE 
                WHEN p.id_selecao_1 = s.id_selecao THEN p.quantidade_gols_selecao_1
                WHEN p.id_selecao_2 = s.id_selecao THEN p.quantidade_gols_selecao_2
                ELSE 0
            END), 0) as "Gols Marcados"
        FROM selecoes s
        LEFT JOIN partidas p ON (p.id_selecao_1 = s.id_selecao OR p.id_selecao_2 = s.id_selecao)
        GROUP BY s.id_selecao
        ORDER BY "Gols Marcados" DESC
        LIMIT 5
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)

def artilheiro_copa():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            j.nome_jogador as "Jogador",
            s.nome_selecao as "Seleção",
            COUNT(g.id_gol) as "Gols"
        FROM gols g
        JOIN jogadores j ON g.id_jogador = j.id_jogador
        JOIN selecoes s ON j.id_selecao = s.id_selecao
        GROUP BY j.id_jogador
        ORDER BY "Gols" DESC
        LIMIT 5
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)

def fair_play():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            s.nome_selecao as "Seleção",
            COALESCE(SUM(CASE WHEN c.tipo_cartao = 'Amarelo' THEN 1 ELSE 0 END), 0) as "Amarelos",
            COALESCE(SUM(CASE WHEN c.tipo_cartao = 'Vermelho' THEN 1 ELSE 0 END), 0) as "Vermelhos",
            COALESCE((SUM(CASE WHEN c.tipo_cartao = 'Amarelo' THEN 1 ELSE 0 END) * 1) + 
            (SUM(CASE WHEN c.tipo_cartao = 'Vermelho' THEN 1 ELSE 0 END) * 3), 0) as "Pontuação"
        FROM selecoes s
        LEFT JOIN jogadores j ON j.id_selecao = s.id_selecao
        LEFT JOIN cartoes c ON c.id_jogador = j.id_jogador
        GROUP BY s.id_selecao
        ORDER BY "Pontuação" ASC
        LIMIT 5
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)


# ==============================================================================
# INTERFACE GRÁFICA DO DASHBOARD (HOME)
# ==============================================================================

st.set_page_config(
    page_title="Dashboard Copa do Mundo 2026",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Painel Analítico - Copa do Mundo 2026")
st.subheader("Sistema de Monitoramento Estatístico Integrado ao MySQL")

# Tratar erros de banco de dados vazio no primeiro carregamento
try:
    # 1. Linha superior de KPIs (Indicadores Importantes)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🗺️ Seleções Cadastradas", contar_selecoes())
    with col2:
        st.metric("🏃 Total de Jogadores", contar_jogadores())
    with col3:
        st.metric("📅 Partidas Agendadas/Jogadas", contar_partidas())
    with col4:
        st.metric("⚽ Total de Gols Marcados", contar_gols())

    st.divider()

    # 2. Seção Gráfica do Painel Principal
    st.markdown("### 📊 Estatísticas Avançadas do Campeonato")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("**🌍 Distribuição de Países por Continente**")
        df_cont = selecoes_por_continente()
        if not df_cont.empty:
            st.bar_chart(df_cont.set_index("Continente"))
            
        st.markdown("**🔥 Seleções com Melhor Desempenho Ofensivo (Mais Gols)**")
        df_gols_mar = selecao_mais_gols()
        if not df_gols_mar.empty:
            st.dataframe(df_gols_mar, use_container_width=True, hide_index=True)

    with col_g2:
        st.markdown("**⭐ Maiores Campeões Mundiais Presentes**")
        df_campeas = top_campeas()
        if not df_campeas.empty:
            st.bar_chart(df_campeas.set_index("Seleção"))

        st.markdown("**🛡️ Solidez Defensiva (Menos Gols Sofridos)**")
        df_gols_sof = defesa_menos_vazada()
        if not df_gols_sof.empty:
            st.dataframe(df_gols_sof, use_container_width=True, hide_index=True)

    st.divider()

    # 3. Seções de Tabelas Auxiliares de Desempenho
    col_tab1, col_tab2 = st.columns(2)
    with col_tab1:
        st.markdown("### 👟 Corrida pela Artilharia")
        df_art = artilheiro_copa()
        if df_art.empty:
            st.info("Aguardando o início dos jogos para registrar os gols.")
        else:
            st.dataframe(df_art, use_container_width=True, hide_index=True)

    with col_tab2:
        st.markdown("### 🕊️ Ranking Fair Play (Menos Faltoso)")
        df_fp = fair_play()
        if df_fp.empty:
            st.info("Nenhum cartão aplicado até o momento.")
        else:
            st.dataframe(df_fp, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Erro ao conectar com o banco de dados. Certifique-se de que o script SQL foi executado. Detalhes: {e}")

# 4. Rodapé Corporativo com a Equipe Oficial
st.sidebar.markdown("""
### 👥 Equipe de Desenvolvimento
* **Arthur Ferreira Barbosa**
* **Guilherme Nery Rocha**
* **Isadora Morais**
* **Kassiane Gomes da Silva**
* **Leandro Augusto Barboza da Silva**
* **Wilka Vitória Granjeiro do Nascimento**

---
💡 *Utilize o menu nativo acima para alternar para as áreas de gerenciamento CRUD das tabelas.*
""")