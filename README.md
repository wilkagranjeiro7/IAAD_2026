# 🏆 Dashboard Copa do Mundo 2026 - Gestão e Análise IAAD

Este repositório contém o projeto prático da disciplina de **Introdução ao Armazenamento e Análise de Dados (IAAD)**. O sistema consiste em um **Dashboard Web** integrado a um banco de dados relacional MySQL para o gerenciamento completo (CRUD) de dados de uma Copa do Mundo sediada na América do Norte.

## 👥 Integrantes da Equipe
* Arthur Ferreira Barbosa
* Guilherme Nery Rocha
* Isadora Morais
* Kassiane Gomes da Silva
* Leandro Augusto Barboza da Silva
* Wilka Vitória Granjeiro do Nascimento

## 🗄️ Estrutura do Projeto
O projeto está organizado de forma modular para facilitar a manutenção e a avaliação:
* **`database/`**: Contém a modelagem do banco (Arquivo `.mwb` do Workbench, imagem do DER e o script `Copa_do_Mundo.sql`).
* **`src/`**: Contém o código-fonte do Dashboard.
  * `Dashboard.py`: Arquivo principal e tela inicial do painel.
  * `conexao.py`: Script responsável pela ponte de comunicação com o MySQL.
  * `pages/`: Subpasta onde ficam as telas de gerenciamento de cada entidade (Seleções, Jogadores, Estádios, Árbitros e Partidas).
* **`testes/`**: Scripts de rascunho utilizados durante o desenvolvimento.

## 🛠️ Tecnologias Utilizadas
* **Banco de Dados:** MySQL v8.0
* **Linguagem:** Python v3.10+
* **Driver de Conexão:** `mysql-connector-python`
* **Manipulação de Dados:** Pandas

---

## 🚀 Como Executar o Projeto Localmente

### 1. Configuração do Banco de Dados (MySQL)
1. Abra o seu gerenciador MySQL (ex: Workbench).
2. Execute o script contido em `database/Copa_do_Mundo.sql` para criar e popular a estrutura das tabelas.

### 2. Instalação das Dependências do Dashboard
No terminal, dentro da pasta raiz do projeto, ative o seu ambiente virtual e instale as bibliotecas:
```bash
pip install streamlit mysql-connector-python pandas