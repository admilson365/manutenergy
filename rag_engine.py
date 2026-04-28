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
            docs.append(Document(page_content=texto))

    return docs


def quebrar_texto(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80
    )
    return splitter.split_documents(docs)


def salvar_memoria(chunks):
    global VECTORSTORE

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    VECTORSTORE = FAISS.from_documents(chunks, embeddings)


def buscar_memoria(pergunta):
    global VECTORSTORE

    if VECTORSTORE is None:
        return "Nenhum documento carregado."

    docs = VECTORSTORE.similarity_search(pergunta, k=3)

    contexto = "\n\n".join([doc.page_content for doc in docs])

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    prompt = f"""
Você é um especialista em manutenção industrial.

Responda de forma objetiva e técnica.

PERGUNTA:
{pergunta}

CONTEXTO EXTRAÍDO DOS MANUAIS:
{contexto}

Responda resumindo e explicando claramente.
"""

    chat = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
      model="llama-3.1-8b-instant"  
    )

    return chat.choices[0].message.content
