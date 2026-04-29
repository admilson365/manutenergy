import streamlit as st
import json
import os
from hashlib import sha256

ARQUIVO_USERS = "users.json"


# ========================
# USERS
# ========================
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USERS):
        with open(ARQUIVO_USERS, "r") as f:
            return json.load(f)
    return {}


def salvar_usuarios(users):
    with open(ARQUIVO_USERS, "w") as f:
        json.dump(users, f)


def hash_senha(senha):
    return sha256(senha.encode()).hexdigest()


# ========================
# INIT SESSION
# ========================
if "logado" not in st.session_state:
    st.session_state.logado = False


usuarios = carregar_usuarios()


# ========================
# LOGIN PAGE
# ========================
if not st.session_state.logado:

    st.title("🔐 ManutEnergy AI Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        if usuario in usuarios and usuarios[usuario] == hash_senha(senha):
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()

        else:
            st.error("Usuário ou senha inválidos")


# ========================
# SISTEMA LOGADO
# ========================
else:

    st.sidebar.success(f"Logado: {st.session_state.usuario}")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    # ========================
    # CADASTRO DE USUÁRIO
    # ========================
    st.sidebar.subheader("👤 Criar usuário")

    novo_user = st.sidebar.text_input("Novo usuário")
    nova_senha = st.sidebar.text_input("Nova senha", type="password")

    if st.sidebar.button("Criar usuário"):

        usuarios = carregar_usuarios()

        if novo_user in usuarios:
            st.sidebar.error("Usuário já existe")
        else:
            usuarios[novo_user] = hash_senha(nova_senha)
            salvar_usuarios(usuarios)
            st.sidebar.success("Usuário criado com sucesso")

    # ========================
    # SISTEMA IA (placeholder)
    # ========================
    st.title("🏭 ManutEnergy AI")

    st.info("Sistema logado funcionando")

    pergunta = st.text_input("Digite sua pergunta")

    if st.button("Consultar") and pergunta:
        st.write("Resposta simulada:", pergunta)
