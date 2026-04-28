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

    if not docs:
        return "Nenhuma informação encontrada."

    resposta = "📄 Resposta técnica localizada:\n\n"

    for i, doc in enumerate(docs, 1):
        trecho = doc.page_content.strip().replace("\n", " ")
        resposta += f"{i}. {trecho[:500]}\n\n"

    return resposta
