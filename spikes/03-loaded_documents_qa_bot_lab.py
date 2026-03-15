# --- LEYENDA ---
# 1.  LangChain Community: PyPDFLoader Chroma RetrievalQA para construir el flujo RAG.
# 2.     LangChain Ollama: OllamaLLM y OllamaEmbeddings para responder y vectorizar con Ollama.
# 3.              Gradio: Interfaz simple para cargar un PDF y hacer preguntas sobre su contenido.

# --- INSTALACION ---
# 1.           Ollama: irm https://ollama.com/install.ps1 | iex.
# 2.  LLM llama3.2:3b: ollama pull llama3.2:3b.
# 3.      Embeddings QA: ollama pull nomic-embed-text.
# 4.       Dependencias: pip install -U gradio langchain langchain-community langchain-ollama chromadb pypdf.

# --- VERIFICACION ---
# 1.           Ollama: ollama --version.
# 2.  Ollama Servidor: ollama serve.
# 3.   Ollama Modelos: ollama list.
# 4.           Gradio: pip show gradio.

# --- DEPENDENCIAS ---
# 1.      Warnings: Para ocultar avisos de la practica mientras se prueba la interfaz.
# 2.        Gradio: Para construir la interfaz visual de carga y consulta.
# 3.  OllamaEmbeddings: Para generar embeddings desde Ollama.
# 4.       OllamaLLM: Para responder preguntas con un modelo local de Ollama.
# 5.  RetrievalQA: Para crear una cadena de pregunta y respuesta con retrieval.
# 6.  TextSplitter: Para dividir el contenido del PDF en fragmentos manejables.
# 7.   PyPDFLoader: Para cargar el contenido del PDF como documentos LangChain.
# 8.         Chroma: Para almacenar y recuperar embeddings en una base vectorial real.
import warnings

import gradio as gr
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

# --- CONFIGURACION ---
# 1. Modelo QA: Modelo local de Ollama para responder preguntas.
# 2. Embeddings QA: Modelo local de Ollama para representar texto en vectores.
# 3. Host Gradio: Direccion para publicar la interfaz.
# 4. Puerto Gradio: Puerto usado por la practica.
MODEL_NAME = "llama3.2:3b"
EMBED_MODEL_NAME = "nomic-embed-text"
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7860
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 50
TOP_K = 4

# --- ESTADO ---
_llm_model = None
_embedding_model = None


# --- WARNINGS ---
# 1.1. Funcion para ocultar warnings durante la ejecucion de la practica.
def warn(*args, **kwargs):
    # Ignora avisos no criticos para mantener la salida mas limpia.
    pass


warnings.warn = warn
warnings.filterwarnings("ignore")


# --- PASO 1: LLM ---
# 2.1. Funcion para cargar el modelo LLM de Ollama.
def get_llm():
    # Reutiliza la misma instancia para evitar recargar el modelo en cada consulta.
    global _llm_model

    if _llm_model is None:
        _llm_model = OllamaLLM(
            model=MODEL_NAME,
            temperature=0.5,
            num_predict=256,
        )

    # Devuelve el LLM listo para la cadena QA.
    return _llm_model


# --- PASO 2: DOCUMENT LOADER ---
# 3.1. Funcion para cargar un PDF como documentos LangChain.
def document_loader(file_path: str):
    # Crea una instancia de PyPDFLoader con el archivo preparado.
    loader = PyPDFLoader(file_path)
    # Lee el contenido del archivo y lo convierte en una lista de documentos o páginas con texto y metadatos.
    loaded_document = loader.load()

    # Devuelve el documento completo cargado desde PDF.
    return loaded_document


# --- PASO 3: TEXT SPLITTER ---

# 4.1. Funcion para partir el texto en trozos.
def text_splitter(data):
    # RecursiveCharacterTextSplitter: Herramienta de LangChain que va a cortar el texto.
    splitter = RecursiveCharacterTextSplitter(
        # Marca el tamano maximo de cada trozo.
        chunk_size=CHUNK_SIZE,
        # Deja un poco de texto repetido entre trozos para seguir el contexto.
        chunk_overlap=CHUNK_OVERLAP,
        # Mide el tamano contando caracteres.
        length_function=len,
    )

    # split_documents: Método de RecursiveCharacterTextSplitter para corta el documento en trozos pequenos.
    chunks = splitter.split_documents(data)

    # Devuelve los trozos generados.
    return chunks



# --- PASO 4: EMBEDDING MODEL ---
# 5.1. Funcion para cargar el modelo de embeddings de Ollama.
def ollama_embedding():
    # Reutiliza la misma instancia para evitar recargar embeddings en cada paso.
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = OllamaEmbeddings(model=EMBED_MODEL_NAME)

    # Devuelve el modelo listo para vectorizar fragmentos.
    return _embedding_model


# --- PASO 5: VECTOR DATABASE ---
# 6.1. Funcion para crear una base vectorial Chroma desde los fragmentos.
def vector_database(chunks):
    # Construye una base vectorial real usando Chroma y embeddings de Ollama.
    embedding_model = ollama_embedding()
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name="loaded_documents_qa_bot",
    )

    # Devuelve la base vectorial lista para retrieval.
    return vectordb


# --- PASO 6: RETRIEVER ---
# 7.1. Funcion para construir el retriever desde el PDF cargado.
def retriever(file_path: str):
    # Encadena carga division vectorizacion y retrieval en un solo punto.
    splits = document_loader(file_path)
    chunks = text_splitter(splits)
    vectordb = vector_database(chunks)
    retriever_obj = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )

    # Devuelve el retriever listo para la cadena QA.
    return retriever_obj


# --- PASO 7: QA CHAIN ---
# 8.1. Funcion para responder preguntas sobre un PDF cargado.
def retriever_qa(file_path: str, query: str) -> str:
    # Valida que exista un archivo antes de ejecutar la cadena.
    if not file_path:
        return "Carga un archivo PDF."

    # Valida que exista una pregunta antes de consultar el modelo.
    if not query or not query.strip():
        return "Escribe una pregunta."

    llm = get_llm()
    retriever_obj = retriever(file_path)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever_obj,
        return_source_documents=False,
    )
    response = qa.invoke({"query": query})

    # Devuelve solo el texto final de la respuesta.
    return response["result"]


# --- INTERFAZ ---
# gr.Interface: Crea una interfaz simple basada en una funcion.
#     fn: Funcion Python que procesa el archivo y la pregunta.
#     inputs: Componentes de entrada para PDF y consulta.
#     outputs: Componente de salida para la respuesta.
#     title: Titulo visible en la interfaz.
#     description: Texto de ayuda para el usuario.
rag_application = gr.Interface(
    fn=retriever_qa,
    flagging_mode="never",
    inputs=[
        gr.File(
            label="Upload PDF File",
            file_count="single",
            file_types=[".pdf"],
            type="filepath",
        ),
        gr.Textbox(
            label="Input Query",
            lines=2,
            placeholder="Type your question here...",
        ),
    ],
    outputs=gr.Textbox(label="Output"),
    title="RAG Chatbot",
    description=(
        "Upload a PDF document and ask any question. "
        "The chatbot will try to answer using the provided document."
    ),
)


if __name__ == "__main__":
    # Lanza la aplicacion usando el host y puerto definidos para la practica.
    rag_application.launch(server_name=SERVER_HOST, server_port=SERVER_PORT)
