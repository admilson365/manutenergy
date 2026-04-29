import streamlit as st
import json
import os
from hashlib import sha256
from PyPDF2 import PdfReader

ARQUIVO_USERS = "users.json"


# =========================
# USERS
# =========================
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USERS):
        with open(ARQUIVO_USERS, "r") as f:
            return json.load(f)
    return {"admin": sha256("1234".encode()).hexdigest()}


def salvar_usuarios(users):
    with open(ARQUIVO_USERS, "w") as f:
        json.dump(users, f)

from hashlib import sha256

def hash_senha(senha):
    return sha256(senha.encode()).hexdigest()


if "logado" not in st.session_state:
    st.session_state.logado = False


usuarios = carregar_usuarios()


# =========================
# LOGIN
# =========================
if not st.session_state.logado:

    st.title("🔐 ManutEnergy AI")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        senha_hash = hash_senha(senha)

        if usuario in usuarios and usuarios[usuario] == senha_hash:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()

        else:
            st.error("Usuário ou senha inválidos")

# =========================
# SISTEMA
# =========================
else:

    st.sidebar.success(f"Logado: {st.session_state.usuario}")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    # -------------------------
    # CADASTRO
    # -------------------------
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

    # -------------------------
    # IA
    # -------------------------
    st.title("🏭 ManutEnergy AI")
    st.subheader("🤖 Assistente Técnico")

    arquivos = st.file_uploader(
        "Envie manuais PDF",
        type=["pdf"],
        accept_multiple_files=True
    )

    pergunta = st.text_input("Digite sua pergunta técnica")

    if st.button("Consultar"):

        texto_total = ""

        if arquivos:

            for arquivo in arquivos:
                reader = PdfReader(arquivo)
                for page in reader.pages:
                    conteudo = page.extract_text()
                    if conteudo:
                        texto_total += conteudo + "\n"

            trechos = []

            if pergunta:
                for palavra in pergunta.lower().split():
                    if palavra in texto_total.lower():
                        idx = texto_total.lower().find(palavra)
                        trecho = texto_total[max(0, idx-80): idx+200]
                        trechos.append(trecho)

            if trechos:
                st.write("📌 Trechos encontrados:")
                for t in trechos:
                    st.write(t)
            else:
                st.warning("Nenhum trecho encontrado no documento.")

        else:
            st.info("📁 Nenhum arquivo enviado")

            if pergunta:
                st.write("Resposta:", pergunta)
