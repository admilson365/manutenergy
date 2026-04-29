from PyPDF2 import PdfReader
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

    # =========================
    # CADASTRO DE USUÁRIO
    # =========================
    st.sidebar.subheader("👤 Criar usuário")

    novo = st.sidebar.text_input("Usuário novo")
    senha_nova = st.sidebar.text_input("Senha nova", type="password")

    if st.sidebar.button("Criar"):

        usuarios = carregar_usuarios()

        if novo in usuarios:
            st.sidebar.error("Usuário já existe")
        else:
            usuarios[novo] = hash_senha(senha_nova)
            salvar_usuarios(usuarios)
            st.sidebar.success("Usuário criado")

    # =========================
    # IA
    # =========================
    st.title("🏭 ManutEnergy AI")

    st.subheader("🤖 Assistente Técnico")

    arquivos = st.file_uploader(
        "Envie manuais PDF",
        type=["pdf"],
        accept_multiple_files=True
    )

    pergunta = st.text_input("Digite sua pergunta técnica")

    if st.button("Consultar"):

        if arquivos:

            texto_total = ""

            for arquivo in arquivos:
                reader = PdfReader(arquivo)
                for page in reader.pages:
                    conteudo = page.extract_text()
                    if conteudo:
                        texto_total += conteudo + "\n"

           if trechos:
    st.write("📌 Trechos encontrados:")

    for t in trechos:
        st.write(t)

else:
    st.warning("Nenhum trecho encontrado no documento.")

# fim da consulta
