import os
from groq import Groq
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTORSTORE = None


def ler_pdf(file):
    reader = PdfReader(file)
    docs = []

    for page in reader.pages:
        texto = page.extract_text()

        if texto:
            texto = " ".join(texto.split())
            docs.append(Document(page_content=texto))

    return docs


def quebrar_texto(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=200
    )
    return splitter.split_documents(docs)


def filtrar_chunks(chunks):
    palavras_ruins = [
        "introdução",
        "sumário",
        "agradecimento",
        "manual de operação",
        "anúncio"
    ]

    filtrados = []

    for c in chunks:
        texto = c.page_content.lower()
        if not any(p in texto for p in palavras_ruins):
            filtrados.append(c)

    return filtrados


def salvar_memoria(chunks):
    global VECTORSTORE

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    chunks = filtrar_chunks(chunks)
    VECTORSTORE = FAISS.from_documents(chunks, embeddings)


def buscar_memoria(pergunta):
    global VECTORSTORE

    if VECTORSTORE is None:
        return "Nenhum documento carregado."

    pergunta = pergunta.lower().strip()

    reforco = f"""
    {pergunta}

    manutenção ajuste regulagem tensionamento corrente sistema mecânico transporte
    """

    docs = VECTORSTORE.similarity_search(pergunta, k=15)

# filtro por palavra-chave (FORTE)
palavras = pergunta.split()

docs_filtrados = []

for doc in docs:
    texto = doc.page_content.lower()
    if any(p in texto for p in palavras):
        docs_filtrados.append(doc)

# fallback se não encontrar nada
if not docs_filtrados:
    docs_filtrados = docs[:5]

    contexto = "\n\n".join([
        doc.page_content
        for doc in docs
        if len(doc.page_content) > 80
    ])

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    prompt = f"""
Você é um engenheiro de manutenção industrial.

Responda direto e técnico.

Use o manual primeiro.
Se não encontrar, use conhecimento de mercado e avise no início:
SUGESTÃO BASEADA EM CONHECIMENTO TÉCNICO DE MERCADO

PERGUNTA:
{pergunta}

CONTEXTO:
{contexto}
"""

    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )

    return chat.choices[0].message.content
