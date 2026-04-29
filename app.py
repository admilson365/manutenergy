import streamlit as st
import json
import os

ARQUIVO_USERS = "users.json"


def carregar_usuarios():
    if os.path.exists(ARQUIVO_USERS):
        with open(ARQUIVO_USERS, "r") as f:
            return json.load(f)
    return {"admin": "1234"}


def salvar_usuarios(users):
    with open(ARQUIVO_USERS, "w") as f:
        json.dump(users, f)


# init
if "logado" not in st.session_state:
    st.session_state.logado = False


usuarios = carregar_usuarios()


# ======================
# LOGIN
# ======================
if not st.session_state.logado:

    st.title("ManutEnergy AI")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        if usuario in usuarios and usuarios[usuario] == senha:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

# ======================
# SISTEMA
# ======================
else:

    st.sidebar.success(f"Logado: {st.session_state.usuario}")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    st.title("🏭 ManutEnergy AI")

    st.info("Sistema funcionando")

    # cadastro simples
    st.sidebar.subheader("Criar usuário")

    novo = st.sidebar.text_input("Novo usuário")
    senha_nova = st.sidebar.text_input("Senha", type="password")

    if st.sidebar.button("Criar"):

        usuarios = carregar_usuarios()

        if novo in usuarios:
            st.sidebar.error("Usuário já existe")
        else:
            usuarios[novo] = senha_nova
            salvar_usuarios(usuarios)
            st.sidebar.success("Criado com sucesso")
