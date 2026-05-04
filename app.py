import streamlit as st
import json
import os
from rag_engine import ler_arquivo, quebrar_texto, salvar_memoria, buscar_memoria
from rag_engine import carregar_memoria

carregar_memoria()

# =========================
# FUNÇÕES
# =========================
def carregar_usuarios():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    with open("users.json", "w") as f:
        json.dump(usuarios, f)

# =========================
# SESSION
# =========================
if "logado" not in st.session_state:
    st.session_state.logado = False

usuarios = carregar_usuarios()

# controle de login
if "logado" not in st.session_state:
    st.session_state.logado = False

# tela de login
if not st.session_state.logado:

    st.title("🔐 Login - ManutEnergy AI")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        print("DEBUG:", usuario, senha)

        if usuario.strip().lower() == "admin" and senha.strip() == "123":
            st.session_state.logado = True
        else:
            st.error("Usuário ou senha inválidos")

    st.stop()

# =========================
# SISTEMA (IA)
# =========================
else:

    st.title("🏭 ManutEnergy AI")

uploaded_files = st.file_uploader(
    "Envie arquivos",
    type=["pdf", "txt", "docx", "pptx"],
    accept_multiple_files=True
)

if uploaded_files:

    todos_chunks = []

    for file in uploaded_files:

        docs = ler_arquivo(file)   # <-- AQUI é a função nova
        chunks = quebrar_texto(docs)

        todos_chunks.extend(chunks)

    salvar_memoria(todos_chunks)
    st.success("Arquivos carregados com sucesso!")

    pergunta = st.text_input("Pergunta técnica")

    if st.button("Consultar"):
        resposta = buscar_memoria(pergunta)
        st.write("📌 Resposta:")
        st.write(resposta)

    # =========================
    # CADASTRO
    # =========================
    st.sidebar.subheader("👤 Criar usuário")

    novo = st.sidebar.text_input("Usuário novo")
    senha_nova = st.sidebar.text_input("Senha nova", type="password")

    if st.sidebar.button("Criar"):

        if novo in usuarios:
            st.sidebar.error("Usuário já existe")
        else:
            usuarios[novo] = senha_nova
            salvar_usuarios(usuarios)
            st.sidebar.success("Usuário criado")
