from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

VECTORSTORE = None


from pypdf import PdfReader
from langchain_core.documents import Document

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
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(docs)


def salvar_memoria(textos):
    global VECTORSTORE

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    VECTORSTORE = FAISS.from_documents(textos, embeddings)

    return VECTORSTORE


def buscar_memoria(pergunta):
    global VECTORSTORE

    if VECTORSTORE is None:
        return []

    docs = VECTORSTORE.similarity_search(pergunta, k=4)

    return [d.page_content for d in docs]
