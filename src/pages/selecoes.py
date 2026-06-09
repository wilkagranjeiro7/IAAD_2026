import streamlit as st
import pandas as pd
from conexao import conectar  # <- CORRIGIDO: Import direto da conexão unificada

# =========================
# FUNÇÕES AUXILIARES DE BANCO
# =========================
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


# ============================================
# TELA PRINCIPAL (EXECUÇÃO DIRETA)
# ============================================
st.header("⚽ Gerenciar Seleções")

# Carregar dados iniciais
df = listar_selecoes()
grupos_df = listar_grupos_aux()

aba_lista, aba_cadastrar, aba_editar = st.tabs(["📋 Lista & Filtros", "➕ Cadastrar Seleção", "🔧 Editar Seleção"])

# ============================================
# ABA 1: LISTAR E FILTRAR SELEÇÕES
# ============================================
with aba_lista:
    if not df.empty:
        # Cards de estatísticas rápidos
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Seleções", len(df))
        with col2:
            st.metric("Continentes Atendidos", df["continente"].nunique())
        with col3:
            campea = df.loc[df["titulos"].idxmax()] if df["titulos"].max() > 0 else None
            titulo = f"{campea['nome_selecao']} ({campea['titulos']})" if campea is not None else "Nenhum"
            st.metric("Maior Campeã", titulo)
        
        st.divider()

        # Filtros organizados
        col_busca, col_cont, col_grp = st.columns([2, 1, 1])
        with col_busca:
            busca = st.text_input("Buscar pelo nome:", placeholder="Digite o país...")
        with col_cont:
            continentes_opcoes = ["Todos"] + sorted(df["continente"].unique().tolist())
            filtro_continente = st.selectbox("Filtrar por Continente:", continentes_opcoes)
        with col_grp:
            grupos_opcoes = ["Todos"] + sorted(grupos_df["nome_grupo"].unique().tolist()) if not grupos_df.empty else ["Todos"]
            filtro_grupo = st.selectbox("Filtrar por Grupo:", grupos_opcoes)

        # Aplicar Filtros no DataFrame
        df_filtrado = df.copy()
        if busca:
            df_filtrado = df_filtrado[df_filtrado["nome_selecao"].str.contains(busca, case=False)]
        if filtro_continente != "Todos":
            df_filtrado = df_filtrado[df_filtrado["continente"] == filtro_continente]
        if filtro_grupo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["nome_grupo"] == filtro_grupo]

        # Exibição Analítica dos Dados Filtrados
        if df_filtrado.empty:
            st.warning("Nenhuma seleção corresponde aos filtros aplicados.")
        else:
            for grupo in sorted(df_filtrado["nome_grupo"].dropna().unique()):
                df_grupo = df_filtrado[df_filtrado["nome_grupo"] == grupo]
                
                st.markdown(f"#### 🏆 GRUPO {grupo}")
                
                # Exibição formatada em Grid
                for _, selecao in df_grupo.iterrows():
                    with st.container():
                        cols = st.columns([2, 1.5, 2, 1.5, 1])
                        with cols[0]:
                            st.markdown(f"**{selecao['nome_selecao']}**")
                        with cols[1]:
                            st.caption(f"🌍 {selecao['continente']}")
                        with cols[2]:
                            st.write(f"👔 {selecao['tecnico']}")
                        with cols[3]:
                            st.write(f"⭐ {selecao['titulos']} título(s)")
                        with cols[4]:
                            if st.button("Excluir", key=f"del_{selecao['id_selecao']}", use_container_width=True):
                                excluir_selecao(selecao['id_selecao'])
                                st.success(f"{selecao['nome_selecao']} foi removida!")
                                st.rerun()
                    st.markdown("---")
    else:
        st.info("Nenhuma seleção cadastrada no banco de dados.")

# ============================================
# ABA 2: CADASTRAR NOVA SELEÇÃO
# ============================================
with aba_cadastrar:
    st.subheader("Nova Seleção")
    if not grupos_df.empty:
        opcoes_grupo = {row["nome_grupo"]: row["id_grupo"] for _, row in grupos_df.iterrows()}
        
        with st.form("form_cadastro"):
            nome_cad = st.text_input("Nome da Seleção (País)", max_chars=50)
            continente_cad = st.selectbox("Continente Sede", ["America", "Europa", "Africa", "Ásia", "Oceania"])
            tecnico_cad = st.text_input("Nome do Técnico", max_chars=50)
            titulos_cad = st.number_input("Quantidade de Títulos Mundiais", min_value=0, step=1)
            grupo_nome_cad = st.selectbox("Definir Grupo da Copa", list(opcoes_grupo.keys()))
            
            if st.form_submit_button("Salvar Seleção", use_container_width=True):
                if nome_cad.strip():
                    inserir_selecao(nome_cad, continente_cad, tecnico_cad, titulos_cad, opcoes_grupo[grupo_nome_cad])
                    st.success(f"Seleção {nome_cad} cadastrada com sucesso!")
                    st.rerun()
                else:
                    st.error("O nome da seleção é obrigatório!")
    else:
        st.warning("Cadastre ao menos um Grupo na aba de grupos antes de adicionar seleções.")

# ============================================
# ABA 3: EDITAR SELEÇÃO EXISTENTE
# ============================================
with aba_editar:
    st.subheader("Modificar Dados")
    if not df.empty and not grupos_df.empty:
        opcoes_selecao = {row["nome_selecao"]: row["id_selecao"] for _, row in df.iterrows()}
        selecao_escolhida = st.selectbox("Selecione o país para editar:", list(opcoes_selecao.keys()))
        
        # Carregar dados atuais do registro selecionado
        registro = buscar_selecao(opcoes_selecao[selecao_escolhida])
        opcoes_grupo = {row["nome_grupo"]: row["id_grupo"] for _, row in grupos_df.iterrows()}
        
        # Identificar os índices atuais para pré-população estável do formulário
        continentes_lista = ["America", "Europa", "Africa", "Ásia", "Oceania"]
        idx_cont = continentes_lista.index(registro["continente"]) if registro["continente"] in continentes_lista else 0
        
        nome_grp_atual = [k for k, v in opcoes_grupo.items() if v == registro["id_grupo"]]
        idx_grp = list(opcoes_grupo.keys()).index(nome_grp_atual[0]) if nome_grp_atual else 0

        with st.form("form_edicao"):
            nome_edit = st.text_input("Nome da Seleção", value=registro["nome_selecao"], max_chars=50)
            continente_edit = st.selectbox("Continente", continentes_lista, index=idx_cont)
            tecnico_edit = st.text_input("Técnico", value=registro["tecnico"], max_chars=50)
            titulos_edit = st.number_input("Títulos", value=int(registro["titulos"]), min_value=0, step=1)
            grupo_nome_edit = st.selectbox("Grupo", list(opcoes_grupo.keys()), index=idx_grp)
            
            if st.form_submit_button("Atualizar Dados", use_container_width=True):
                if nome_edit.strip():
                    atualizar_selecao(registro["id_selecao"], nome_edit, continente_edit, tecnico_edit, titulos_edit, opcoes_grupo[grupo_nome_edit])
                    st.success(f"Seleção {nome_edit} atualizada com sucesso!")
                    st.rerun()
                else:
                    st.error("O nome da seleção não pode ficar em branco!")
    else:
        st.warning("Não há dados suficientes disponíveis para realizar edições.")