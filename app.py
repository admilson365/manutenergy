import streamlit as st
import json
import os

from rag_engine import (ler_pdf,quebrar_texto,salvar_memoria,buscar_memoria)
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


# =========================
# LOGIN
# =========================
if not st.session_state.logado:

    st.title("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        if usuario in usuarios and usuarios[usuario] == senha:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")


# =========================
# SISTEMA (IA)
# =========================
else:

    st.title("🏭 ManutEnergy AI")

    arquivo = st.file_uploader("Envie PDF", type=["pdf"])

    if arquivo:
        docs = ler_pdf(arquivo)
        chunks = quebrar_texto(docs)
        salvar_memoria(chunks)

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
            usuarios[novo] = hash_senha(senha_nova)
            salvar_usuarios(usuarios)
            st.sidebar.success("Usuário criado")

st.success("admin resetado")
