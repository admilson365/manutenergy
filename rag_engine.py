import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

embeddings = OpenAIEmbeddings()

def ler_pdf(caminho_arquivo):
    loader = PyPDFLoader(caminho_arquivo)
    return loader.load()

def quebrar_texto(paginas):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(paginas)

def salvar_memoria(partes, caminho="storage/faiss_index"):
    if os.path.exists(caminho):
        db = FAISS.load_local(caminho, embeddings, allow_dangerous_deserialization=True)
        db.add_documents(partes)
    else:
        db = FAISS.from_documents(partes, embeddings)

    db.save_local(caminho)

def buscar_memoria(pergunta, caminho="storage/faiss_index"):
    db = FAISS.load_local(caminho, embeddings, allow_dangerous_deserialization=True)
    return db.similarity_search(pergunta, k=4)
