from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

VECTORSTORE = None


def ler_pdf(caminho):
    loader = PyPDFLoader(caminho)
    return loader.load()


def quebrar_texto(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(docs)


def salvar_memoria(textos):
    global VECTORSTORE

    embeddings = OpenAIEmbeddings()

    VECTORSTORE = FAISS.from_documents(textos, embeddings)

    return VECTORSTORE


def buscar_memoria(pergunta):
    global VECTORSTORE

    if VECTORSTORE is None:
        return []

    docs = VECTORSTORE.similarity_search(pergunta, k=4)

    return [d.page_content for d in docs]
