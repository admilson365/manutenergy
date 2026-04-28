import streamlit as st
import streamlit_authenticator as stauth
from rag_engine import ler_pdf, quebrar_texto, salvar_memoria, buscar_memoria

st.set_page_config(page_title="ManutEnergy AI", layout="wide")

# USUÁRIOS
names = ["Admilson", "Tecnico 1", "Supervisor"]
usernames = ["admin", "tecnico1", "supervisor"]

passwords = ["1234", "1234", "1234"]

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "manutenergy_cookie",
    "abcdef",
    cookie_expiry_days=7
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Usuário ou senha incorretos")

elif authentication_status == None:
    st.warning("Digite usuário e senha")

elif authentication_status:

    authenticator.logout("Sair", "sidebar")

    st.title("🏭 ManutEnergy AI")
    st.success(f"Bem-vindo, {name}")

    arquivos = st.file_uploader(
        "Envie manuais PDF",
        type=["pdf"],
        accept_multiple_files=True
    )

    if arquivos:
        docs_total = []

        for arquivo in arquivos:
            docs = ler_pdf(arquivo)
            docs_total.extend(docs)

        chunks = quebrar_texto(docs_total)
        salvar_memoria(chunks)

        st.success("Arquivos carregados.")

    pergunta = st.text_input("Digite sua pergunta técnica")

    if st.button("Consultar"):

        if pergunta:
            resposta = buscar_memoria(pergunta)
            st.write(resposta)
