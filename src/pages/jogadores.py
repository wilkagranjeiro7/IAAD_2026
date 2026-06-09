import streamlit as st
import pandas as pd
from conexao import conectar 

# =========================
# FUNÇÃO AUXILIAR: LISTAR SELEÇÕES PARA O SELECTBOX
# =========================
def listar_selecoes_combo():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_selecao, nome_selecao FROM selecoes ORDER BY nome_selecao")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados


# =========================
# LISTAR JOGADORES
# =========================
def listar_jogadores():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            j.id_jogador,
            j.nome_jogador,
            j.posicao,
            j.numero_camisa,
            j.data_nascimento,
            s.nome_selecao
        FROM jogadores j
        JOIN selecoes s ON j.id_selecao = s.id_selecao
        ORDER BY s.nome_selecao, j.numero_camisa
    """)
    
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return pd.DataFrame(dados)


# =========================
# INSERIR JOGADOR
# =========================
def inserir_jogador(nome, posicao, camisa, nascimento, id_selecao):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO jogadores 
        (nome_jogador, posicao, numero_camisa, data_nascimento, id_selecao)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, posicao, camisa, nascimento, id_selecao))
    
    conexao.commit()
    cursor.close()
    conexao.close()


# =========================
# BUSCAR JOGADOR POR ID
# =========================
def buscar_jogador(id_jogador):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM jogadores WHERE id_jogador = %s
    """, (id_jogador,))
    
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado


# =========================
# ATUALIZAR JOGADOR
# =========================
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


# =========================
# EXCLUIR JOGADOR
# =========================
def excluir_jogador(id_jogador):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("DELETE FROM jogadores WHERE id_jogador = %s", (id_jogador,))
    
    conexao.commit()
    cursor.close()
    conexao.close()


# ============================================
# TELA DE JOGADORES (EXECUÇÃO DIRETA)
# ============================================
# CORRIGIDO: Retirado o def tela_jogadores() e o botão voltar manual.

st.header("👤 Gerenciar Jogadores")

df = listar_jogadores()
selecoes_disponiveis = listar_selecoes_combo()

aba1, aba2, aba3 = st.tabs(["Cadastrar", "Editar", "Excluir"])

# =========================
# CADASTRAR
# =========================
with aba1:
    st.subheader("Novo Jogador")
    
    if selecoes_disponiveis:
        nome = st.text_input("Nome do Jogador", key="j_nome")
        posicao = st.selectbox(
            "Posição",
            ["Goleiro", "Zagueiro", "Lateral Direito", "Lateral Esquerdo", "Volante", "Meio Campo", "Atacante", "Centroavante", "Ponta Direita", "Ponta Esquerda"],
            key="j_posicao"
        )
        camisa = st.number_input("Número da Camisa", min_value=1, max_value=99, key="j_camisa")
        nascimento = st.date_input("Data de Nascimento", key="j_nascimento")
        
        opcoes = {s["nome_selecao"]: s["id_selecao"] for s in selecoes_disponiveis}
        selecao = st.selectbox("Seleção", list(opcoes.keys()), key="j_selecao")
        
        if st.button("Cadastrar Jogador", key="btn_cad_jogador"):
            if nome:
                inserir_jogador(nome, posicao, camisa, nascimento, opcoes[selecao])
                st.success("Jogador cadastrado!")
                st.rerun()
            else:
                st.error("Por favor, digite o nome do jogador.")
    else:
        st.warning("Cadastre uma Seleção primeiro antes de adicionar jogadores.")

# =========================
# EDITAR
# =========================
with aba2:
    st.subheader("Editar Jogador")
    
    if not df.empty and selecoes_disponiveis:
        opcoes_jogador = {f"{linha['nome_jogador']} ({linha['nome_selecao']})": linha["id_jogador"] for _, linha in df.iterrows()}
        jogador_escolhido = st.selectbox("Jogador", list(opcoes_jogador.keys()), key="editar_jogador")
        registro = buscar_jogador(opcoes_jogador[jogador_escolhido])
        
        nome_edit = st.text_input("Nome", value=registro["nome_jogador"], key="edit_nome_jogador")
        posicao_edit = st.selectbox(
            "Posição",
            ["Goleiro", "Zagueiro", "Lateral Direito", "Lateral Esquerdo", "Volante", "Meio Campo", "Atacante", "Centroavante", "Ponta Direita", "Ponta Esquerda"],
            key="edit_posicao_jogador"
        )
        camisa_edit = st.number_input("Camisa", min_value=1, max_value=99, value=int(registro["numero_camisa"]), key="edit_camisa")
        nascimento_edit = st.date_input("Nascimento", value=registro["data_nascimento"], key="edit_nascimento")
        
        opcoes_sel = {s["nome_selecao"]: s["id_selecao"] for s in selecoes_disponiveis}
        
        # Encontrar o nome da seleção atual para deixar pré-selecionado
        nome_sel_atual = [k for k, v in opcoes_sel.items() if v == registro["id_selecao"]]
        index_sel = list(opcoes_sel.keys()).index(nome_sel_atual[0]) if nome_sel_atual else 0
        
        selecao_edit = st.selectbox("Seleção", list(opcoes_sel.keys()), index=index_sel, key="edit_selecao")
        
        if st.button("Atualizar Jogador", key="btn_update_jogador"):
            atualizar_jogador(registro["id_jogador"], nome_edit, posicao_edit, camisa_edit, nascimento_edit, opcoes_sel[selecao_edit])
            st.success("Jogador updated!")
            st.rerun()
    else:
        st.warning("Nenhum jogador ou seleção disponível para edição.")

# =========================
# EXCLUIR
# =========================
with aba3:
    st.subheader("Excluir Jogador")
    
    if not df.empty:
        opcoes_jogador = {f"{linha['nome_jogador']} ({linha['nome_selecao']})": linha["id_jogador"] for _, linha in df.iterrows()}
        jogador_del = st.selectbox("Jogador", list(opcoes_jogador.keys()), key="excluir_jogador")
        
        if st.button("Excluir Jogador", key="btn_delete_jogador"):
            excluir_jogador(opcoes_jogador[jogador_del])
            st.success("Jogador removido!")
            st.rerun()
    else:
        st.warning("Nenhum jogador cadastrado.")

# =========================
# TABELA DE JOGADORES
# =========================
st.divider()
st.subheader("📋 Jogadores Cadastrados")

if df.empty:
    st.warning("Nenhum jogador cadastrado.")
else:
    df_exibicao = df.rename(columns={
        "id_jogador": "ID",
        "nome_jogador": "Nome do Jogador",
        "posicao": "Posição",
        "numero_camisa": "Camisa",
        "data_nascimento": "Nascimento",
        "nome_selecao": "Seleção"
    })
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)