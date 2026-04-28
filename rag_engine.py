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
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(docs)


def salvar_memoria(textos):
    global VECTORSTORE

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    VECTORSTORE = FAISS.from_documents(textos, embeddings)

def buscar_memoria(pergunta):
    global VECTORSTORE

    if VECTORSTORE is None:
        return "📁 Nenhum arquivo foi carregado ainda."

    docs = VECTORSTORE.similarity_search(pergunta, k=2)

    if not docs:
        return "❌ Nenhuma informação relevante encontrada."

    contexto = " ".join([doc.page_content for doc in docs])

    pergunta_lower = pergunta.lower()

    if "lubrificação" in pergunta_lower or "lubrificar" in pergunta_lower:
        return f"🔧 Com base no manual analisado, a informação relacionada à lubrificação é:\n\n{contexto}"

    elif "manutenção" in pergunta_lower:
        return f"🛠️ Informações de manutenção encontradas:\n\n{contexto}"

    elif "segurança" in pergunta_lower:
        return f"⚠️ Orientações de segurança localizadas:\n\n{contexto}"

    elif "falha" in pergunta_lower or "erro" in pergunta_lower:
        return f"🚨 Possíveis informações sobre falhas ou erros:\n\n{contexto}"

    else:
        return f"📄 Com base nos documentos carregados, encontrei o seguinte:\n\n{contexto}"
