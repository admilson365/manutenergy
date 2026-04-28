# app.py
# ManutEnergy AI - Piloto Streamlit
# Instalar dependências no requirements.txt:
# streamlit
# PyPDF2
# openai (opcional para IA real)

import streamlit as st
import os
from pypdf import PdfReader

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="ManutEnergy AI",
    page_icon="⚙️",
    layout="wide"
)

# ---------------- CSS INDUSTRIAL VERDE ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0f1117;
    color: white;
    font-family: Arial, sans-serif;
}
.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #35ff8a;
}
.sub-title {
    color: #9ef7c2;
    font-size: 18px;
}
.stTextInput>div>div>input {
    background-color: #1c1f26;
    color: white;
}
.stTextArea textarea {
    background-color: #1c1f26;
    color: white;
}
.block {
    background-color: #161a22;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #2e8b57;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ ManutEnergy AI")
planta = st.sidebar.selectbox(
    "Selecione a Planta:",
    ["Limeira", "Rio Claro", "Recife", "Outra"]
)

menu = st.sidebar.radio(
    "Menu",
    ["Assistente Técnico", "Biblioteca", "Indicadores", "Sobre"]
)

# ---------------- FUNÇÃO LER PDF ----------------
def extrair_texto_pdf(uploaded_files):
    texto_total = ""
    for file in uploaded_files:
        reader = PdfReader(file)
        for page in reader.pages:
            texto_total += page.extract_text() + "\n"
    return texto_total

# ---------------- TELA PRINCIPAL ----------------
st.markdown('<div class="main-title">⚙️ ManutEnergy AI</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">IA Industrial da planta: {planta}</div>', unsafe_allow_html=True)
st.write("")

# ---------------- ASSISTENTE ----------------
if menu == "Assistente Técnico":
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.subheader("🤖 Chat Técnico")

    pergunta = st.text_input("Digite sua pergunta:")

    arquivos = st.file_uploader(
        "Envie manuais PDF para consulta:",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Consultar"):
        if pergunta:
            resposta = f"Pergunta recebida: {pergunta}\n\n"

            if arquivos:
                texto = extrair_texto_pdf(arquivos)

                if pergunta.lower() in texto.lower():
                    resposta += "📄 Informação encontrada nos arquivos internos."
                else:
                    resposta += "🌐 Informação não localizada nos arquivos. Sugestão: consultar base externa."
            else:
                resposta += "📁 Nenhum arquivo enviado. Resposta baseada em conhecimento geral."

            st.success(resposta)
        else:
            st.warning("Digite uma pergunta.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- BIBLIOTECA ----------------
elif menu == "Biblioteca":
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.subheader("📚 Biblioteca Técnica")
    st.write("""
    Utilize esta área para enviar:
    - Manuais PDF
    - Catálogos
    - Lista de peças
    - Procedimentos
    - Diagramas
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- INDICADORES ----------------
elif menu == "Indicadores":
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.subheader("📈 Indicadores")
    st.metric("Equipamentos Cadastrados", "120")
    st.metric("Arquivos Técnicos", "58")
    st.metric("Consultas Hoje", "14")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SOBRE ----------------
elif menu == "Sobre":
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.subheader("🏭 Sobre o Projeto")
    st.write("""
    Plataforma piloto para suporte técnico da manutenção industrial.

    Objetivos:
    - Informações rápidas
    - Manuais na palma da mão
    - Apoio técnico aos colaboradores
    - Evolução para IA corporativa multiplantas
    """)
    st.markdown('</div>', unsafe_allow_html=True)
