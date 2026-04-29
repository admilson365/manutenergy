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

    # busca ampla inicial
    docs = VECTORSTORE.similarity_search(pergunta, k=15)

    # filtro por palavra-chave (busca híbrida)
    palavras = pergunta.split()
    docs_filtrados = []

    for doc in docs:
        texto = doc.page_content.lower()
        if any(p in texto for p in palavras):
            docs_filtrados.append(doc)

    # fallback se não encontrar nada relevante
    if not docs_filtrados:
        docs_filtrados = docs[:5]

    # monta contexto
    contexto = "\n\n".join([
        doc.page_content
        for doc in docs_filtrados[:5]
    ])

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    prompt = f"""
Você é um especialista de manutenção industrial.

OBJETIVO:
Encontrar a resposta EXATA dentro do texto.

REGRAS:
- NÃO explique demais
- NÃO copie trechos grandes
- NÃO invente
- Se encontrar a informação, responda direto em 1 ou 2 linhas
- Se não encontrar, diga:
  "Informação não encontrada no manual"

PROCESSO:
1. Procure no texto valores, números, unidades
2. Responda apenas o que foi perguntado

PERGUNTA:
{pergunta}

TEXTO:
{contexto}
"""

    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )

    return f"--- CONTEXTO ENCONTRADO ---\n{contexto}\n\n--- RESPOSTA ---\n{chat.choices[0].message.content}"
