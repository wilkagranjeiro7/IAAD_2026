import streamlit as st
import pandas as pd
from conexao import conectar 

# =========================
# FUNÇÕES AUXILIARES PARA POPULAR OS SELECTBOXES
# =========================
def buscar_selecoes_aux():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_selecao, nome_selecao FROM selecoes ORDER BY nome_selecao")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)

def buscar_estadios_aux():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_estadio, nome_estadio FROM estadios ORDER BY nome_estadio")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)

def buscar_arbitros_aux():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_arbitro, nome_arbitro FROM arbitros ORDER BY nome_arbitro")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)

# =========================
# LISTAR PARTIDAS
# =========================
def listar_partidas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id_partida,
            p.data_partida,
            s1.nome_selecao AS selecao_1,
            s2.nome_selecao AS selecao_2,
            e.nome_estadio,
            a.nome_arbitro,
            p.quantidade_gols_selecao_1,
            p.quantidade_gols_selecao_2,
            p.vencedor
        FROM partidas p
        INNER JOIN selecoes s1 ON p.id_selecao_1 = s1.id_selecao
        INNER JOIN selecoes s2 ON p.id_selecao_2 = s2.id_selecao
        INNER JOIN estadios e ON p.id_estadio = e.id_estadio
        INNER JOIN arbitros a ON p.id_arbitro = a.id_arbitro
        ORDER BY p.data_partida DESC
    """)

    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)


# =========================
# INSERIR PARTIDA
# =========================
def inserir_partida(data_partida, id_estadio, id_selecao_1, id_selecao_2, id_arbitro, gols1, gols2, vencedor):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO partidas
        (data_partida, id_estadio, id_selecao_1, id_selecao_2, id_arbitro, quantidade_gols_selecao_1, quantidade_gols_selecao_2, vencedor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (data_partida, id_estadio, id_selecao_1, id_selecao_2, id_arbitro, gols1, gols2, vencedor))

    conexao.commit()
    cursor.close()
    conexao.close()


# =========================
# EXCLUIR PARTIDA
# =========================
def excluir_partida(id_partida):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM partidas WHERE id_partida = %s", (id_partida,))
    conexao.commit()
    cursor.close()
    conexao.close()


# ============================================
# TELA DE PARTIDAS (EXECUÇÃO DIRETA)
# ============================================
# CORRIGIDO: Retirada a função de envelope e o botão voltar manual.
st.header("⚽ Partidas da Copa")

# Buscar dados de tabelas relacionadas com segurança
df_partidas = listar_partidas()
df_selecoes = buscar_selecoes_aux()
df_estadios = buscar_estadios_aux()
df_arbitros = buscar_arbitros_aux()

# Abas organizadas para evitar misturar cadastro com exclusão na tela
aba1, aba2, aba3 = st.tabs(["Cadastrar Partida", "Visualizar Calendário", "Excluir Registro"])

# =========================
# CADASTRAR NOVA PARTIDA
# =========================
with aba1:
    if not df_selecoes.empty and not df_estadios.empty and not df_arbitros.empty:
        selecao_dict = {s["nome_selecao"]: s["id_selecao"] for _, s in df_selecoes.iterrows()}
        estadio_dict = {e["nome_estadio"]: e["id_estadio"] for _, e in df_estadios.iterrows()}
        arbitro_dict = {a["nome_arbitro"]: a["id_arbitro"] for _, a in df_arbitros.iterrows()}
        
        st.subheader("Registrar Novo Confronto")
        
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
        
        # Lógica automática do vencedor
        if g1 > g2:
            vencedor = selecao_dict[s1]
        elif g2 > g1:
            vencedor = selecao_dict[s2]
        else:
            vencedor = None  # Empate
        
        if st.button("Salvar Partida no Banco"):
            if s1 == s2:
                st.error("Uma seleção não pode jogar contra ela mesma!")
            else:
                inserir_partida(data, estadio_dict[estadio], selecao_dict[s1], selecao_dict[s2], arbitro_dict[arbitro], g1, g2, vencedor)
                st.success("Partida registrada com sucesso!")
                st.rerun()
    else:
        st.warning("Certifique-se de que existem seleções, estádios e árbitros cadastrados antes de criar uma partida.")

# =========================
# LISTAR PARTIDAS
# =========================
with aba2:
    st.subheader("📋 Tabela de Jogos")
    
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
        # Formatando a ordem das colunas para melhor visualização analítica
        st.dataframe(df_exibir[['Data', 'Seleção 1', 'Placar 1', 'Placar 2', 'Seleção 2', 'Estádio Sede', 'Árbitro']], use_container_width=True, hide_index=True)

# =========================
# EXCLUIR PARTIDA
# =========================
with aba3:
    st.subheader("Excluir Histórico")
    
    if not df_partidas.empty:
        partidas_dict = {
            f"{row['selecao_1']} {row['quantidade_gols_selecao_1']} x {row['quantidade_gols_selecao_2']} {row['selecao_2']} ({row['data_partida']})": row["id_partida"]
            for _, row in df_partidas.iterrows()
        }
        
        escolha = st.selectbox("Selecione a partida para apagar", list(partidas_dict.keys()), key="p_del")
        
        if st.button("Excluir Registro Definitivamente"):
            excluir_partida(partidas_dict[escolha])
            st.success("Partida removida do banco de dados!")
            st.rerun()
    else:
        st.warning("Nenhuma partida registrada disponível para exclusão.")