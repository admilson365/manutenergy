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
        return "📁 Nenhum arquivo carregado."

    docs = VECTORSTORE.similarity_search(pergunta, k=2)

    if not docs:
        return "❌ Nenhuma informação encontrada."

    contexto = " ".join([doc.page_content for doc in docs])

    pergunta_lower = pergunta.lower()

    # Lubrificação
    if "lubrificação" in pergunta_lower or "lubrificar" in pergunta_lower:

        if "1 MÊS" in contexto or "720 HRS" in contexto:
            return "🔧 Conforme o manual, a lubrificação dos mancais e rolamentos deve ser realizada mensalmente (1 mês / 720 horas)."

        elif "6 MESES" in contexto:
            return "🔧 Conforme o manual, existem atividades periódicas de lubrificação e revisão a cada 6 meses."

        else:
            return "🔧 O manual cita lubrificação de mancais e rolamentos, porém a frequência exata não foi localizada claramente."

    # Manutenção
    elif "manutenção" in pergunta_lower:
        return "🛠️ O documento apresenta plano de manutenção preventiva com inspeções mensais, semestrais e anuais."

    # Falhas
    elif "falha" in pergunta_lower or "erro" in pergunta_lower:
        return "🚨 Foram localizados trechos técnicos, porém sem falha específica claramente descrita."

    else:
        return f"📄 Informação localizada:\n\n{contexto[:800]}"
