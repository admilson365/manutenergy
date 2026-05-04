import os
from groq import Groq
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from pptx import Presentation
VECTORSTORE = None
DB_PATH = "vectorstore"

def carregar_memoria():
    global VECTORSTORE

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(DB_PATH):
        VECTORSTORE = FAISS.load_local(DB_PATH, embeddings)
def ler_arquivo(file):
    docs = []

    # PDF
    if file.type == "application/pdf":
        reader = PdfReader(file)

        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                texto = " ".join(texto.split())
                docs.append(Document(page_content=texto))

    # TXT
    elif file.type == "text/plain":
        texto = str(file.read(), "utf-8")
        docs.append(Document(page_content=texto))

    # DOCX
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = DocxDocument(file)

        texto = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        docs.append(Document(page_content=texto))

    # PPTX
    elif file.type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
        prs = Presentation(file)

        texto_total = ""

        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text:
                    texto_total += shape.text + "\n"

        docs.append(Document(page_content=texto_total))

    return docs
    for page in reader.pages:
        texto = page.extract_text()

        if texto:
            import re
            texto = re.sub(r'\s+', ' ', texto) 
            docs.append(Document(page_content=texto))

    return docs


def quebrar_texto(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=300
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
    # palavras importantes da pergunta
    stopwords = ["qual", "quais", "o", "a", "os", "as", "de", "da", "do", "das", "dos", "é", "em", "para", "com"]

    palavras = [
        p for p in pergunta.split()
        if p not in stopwords and len(p) > 2
    ]

    # busca inicial
    docs = VECTORSTORE.similarity_search(pergunta, k=20)
     
    palavras = pergunta.lower().split()

    docs_filtrados = []

for doc in docs:
    texto = doc.page_content.lower()

    if any(p in texto for p in palavras):
        docs_filtrados.append(doc)

    if docs_filtrados:
        docs = docs_filtrados
    

    # fallback se não encontrar nada relevante
    if not docs_filtrados:
        docs_filtrados = docs[:8]

    # monta contexto
    contexto = "\n\n".join([
        doc.page_content
        for doc in docs_filtrados[:3]
    ])
    print(contexto)
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    prompt = f"""
Você é um especialista de manutenção industrial.

OBJETIVO:
Responder corretamente com base no tipo de pergunta.

REGRAS:

1. Se a pergunta for sobre VALOR (pressão, temperatura, rpm, corrente, frequência, etc):
- Responder direto com número + unidade
- Máximo 1 linha
- Ex: -5 mmCa a -10 mmCa

2. Se a pergunta for sobre PROCEDIMENTO ou FUNCIONAMENTO:
- Responder de forma técnica e objetiva
- Máximo 5 linhas
- Sem enrolação

3. NÃO copiar texto bruto do manual
4. NÃO inventar informação
5. Se não encontrar no manual:
Responder:
"SUGESTÃO BASEADA EM CONHECIMENTO TÉCNICO DE MERCADO"
e dar a melhor resposta possível

PERGUNTA:
{pergunta}

TEXTO:
{contexto}
"""

    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )

    resposta = chat.choices[0].message.content

    return resposta
