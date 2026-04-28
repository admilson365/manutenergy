import streamlit as st
from rag_engine import ler_pdf, quebrar_texto, salvar_memoria, buscar_memoria

st.set_page_config(page_title="ManutEnergy AI", layout="wide")

# LOGIN SIMPLES
usuarios = {
    "admin": "1234",
    "tecnico1": "1234",
    "supervisor": "1234"
}

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:

    st.title("🔐 Login - ManutEnergy AI")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        if usuario in usuarios and usuarios[usuario] == senha:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

else:

    st.sidebar.success(f"Logado: {st.session_state.usuario}")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    st.title("🏭 ManutEnergy AI")

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

        st.success("Arquivos processados.")

    pergunta = st.text_input("Digite sua pergunta técnica")

    if st.button("Consultar"):

        if pergunta:
            resposta = buscar_memoria(pergunta)
            st.write(resposta)
