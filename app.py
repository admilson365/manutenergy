import streamlit as st
from rag_engine import ler_pdf, quebrar_texto, salvar_memoria, buscar_memoria

st.set_page_config(
    page_title="ManutEnergy AI",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
.block {
    background: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 0 15px rgba(0,0,0,0.15);
}
h1 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🏭 ManutEnergy AI")
st.caption("Plataforma Inteligente de Manutenção Industrial")

st.markdown('<div class="block">', unsafe_allow_html=True)

st.subheader("📁 Upload de Manuais / Procedimentos")

arquivos = st.file_uploader(
    "Envie arquivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)

if arquivos:
    todos_docs = []

    for arquivo in arquivos:
        docs = ler_pdf(arquivo)
        todos_docs.extend(docs)

    chunks = quebrar_texto(todos_docs)
    salvar_memoria(chunks)

    st.success("Arquivos processados com sucesso.")

st.subheader("🤖 Assistente Técnico")

pergunta = st.text_input("Digite sua pergunta técnica:")

if st.button("Consultar"):

    if pergunta:
        resposta = buscar_memoria(pergunta)
        st.write(resposta)
    else:
        st.warning("Digite uma pergunta.")

st.markdown('</div>', unsafe_allow_html=True)
