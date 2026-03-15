# --- LEYENDA ---
# 1. LangChain Community: PyPDFLoader Chroma RetrievalQA para construir el flujo RAG.
# 2.    LangChain Ollama: OllamaLLM y OllamaEmbeddings para responder y vectorizar con Ollama.
# 3.              Gradio: Interfaz simple para cargar un PDF y hacer preguntas sobre su contenido.

# --- INSTALACION ---
# 1.              Ollama: irm https://ollama.com/install.ps1 | iex.
# 2.     LLM llama3.2:3b: ollama pull llama3.2:3b.
# 3.       Embeddings QA: ollama pull nomic-embed-text.
# 4.        Dependencias: pip install -U gradio langchain langchain-community langchain-ollama chromadb pypdf.

# --- VERIFICACION ---
# 1.              Ollama: ollama --version.
# 2.     Ollama Servidor: ollama serve.
# 3.      Ollama Modelos: ollama list.
# 4.              Gradio: pip show gradio.

# --- DEPENDENCIAS ---
# 1.            Warnings: Para ocultar avisos de la practica mientras se prueba la interfaz.
# 2.              Gradio: Para construir la interfaz visual de carga y consulta.
# 3.    OllamaEmbeddings: Para generar embeddings desde Ollama.
# 4.           OllamaLLM: Para responder preguntas con un modelo local de Ollama.
# 5.         RetrievalQA: Para crear una cadena de pregunta y respuesta con retrieval.
# 6.        TextSplitter: Para dividir el contenido del PDF en fragmentos manejables.
# 7.         PyPDFLoader: Para cargar el contenido del PDF como documentos LangChain.
# 8.              Chroma: Para almacenar y recuperar embeddings en una base vectorial real.
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
# Define la direccion donde se publicara la interfaz.
SERVER_HOST = "0.0.0.0"
# Define el puerto donde se abrira la interfaz.
SERVER_PORT = 7860
# Define el tamano maximo de cada trozo.
CHUNK_SIZE = 1000
# Define el texto repetido entre trozos seguidos.
CHUNK_OVERLAP = 50
# Define cuantos trozos recupera la busqueda.
TOP_K = 4

# --- ESTADO ---
# Guarda el modelo de lenguaje ya cargado.
_llm_model = None
# Guarda el modelo de embeddings ya cargado.
_embedding_model = None
# Guarda la ruta del PDF ya indexado.
_indexed_pdf_path = None
# Guarda la base vectorial ya creada.
_vector_store = None
# Guarda el retriever ya creado.
_rag_retriever = None

# --- WARNINGS ---
# 1.1. Funcion para ocultar warnings durante la ejecucion de la practica.
def warn(*args, **kwargs):
    # Ignora avisos no criticos para mantener la salida mas limpia.
    pass

# Reemplaza la funcion original de warnings.
warnings.warn = warn
# Oculta los warnings durante la practica.
warnings.filterwarnings("ignore")

# --- PASO 1: LLM ---
# 2.1. Funcion para cargar el modelo LLM de Ollama.
def get_llm():
    # Reutiliza la misma instancia para evitar recargar el modelo en cada consulta.
    global _llm_model

    # Carga el modelo solo la primera vez.
    if _llm_model is None:
        # Crea el modelo de Ollama para responder preguntas.
        _llm_model = OllamaLLM(
            # Usa el nombre del modelo configurado.
            model=MODEL_NAME,
            # Ajusta la variacion de la respuesta.
            temperature=0.5,
            # Limita la longitud maxima de la salida.
            num_predict=256,
        )

    # Devuelve el LLM listo para la cadena QA.
    return _llm_model

# --- PASO 2: DOCUMENT LOADER ---
# 3.1. Funcion para cargar un PDF como documentos LangChain.
def document_loader(file_path: str):
    # Crea una instancia de PyPDFLoader con el archivo preparado.
    loader = PyPDFLoader(file_path)
    # Lee el contenido del archivo y lo convierte en una lista de documentos con texto y metadatos.
    loaded_document = loader.load()

    # Devuelve el documento completo cargado desde PDF.
    return loaded_document

# --- PASO 3: TEXT SPLITTER ---
# 4.1. Funcion para partir el texto en trozos.
def text_splitter(data):
    # Crea la herramienta de LangChain que corta el texto.
    splitter = RecursiveCharacterTextSplitter(
        # Marca el tamano maximo de cada trozo.
        chunk_size=CHUNK_SIZE,
        # Deja un poco de texto repetido entre trozos para seguir el contexto.
        chunk_overlap=CHUNK_OVERLAP,
        # Mide el tamano contando caracteres.
        length_function=len,
    )

    # Usa el metodo de LangChain para cortar el documento en trozos pequenos.
    chunks = splitter.split_documents(data)

    # Devuelve los trozos generados.
    return chunks

# --- PASO 4: INGESTA ---
# 5.1. Funcion para preparar los trozos del PDF.
def prepare_chunks(file_path: str):
    # Carga el PDF y obtiene sus documentos.
    loaded_documents = document_loader(file_path)
    # Parte esos documentos en trozos pequenos.
    chunks = text_splitter(loaded_documents)

    # Devuelve los trozos listos para indexar.
    return chunks

# --- PASO 5: EMBEDDING MODEL ---
# 6.1. Funcion para cargar el modelo de embeddings de Ollama.
def ollama_embedding():
    # Reutiliza la misma instancia para evitar recargar embeddings en cada paso.
    global _embedding_model

    # Carga el modelo solo la primera vez.
    if _embedding_model is None:
        # Crea el modelo que convierte texto en vectores.
        _embedding_model = OllamaEmbeddings(
            # Usa el nombre del modelo de embeddings configurado.
            model=EMBED_MODEL_NAME,
        )

    # Devuelve el modelo listo para vectorizar fragmentos.
    return _embedding_model

# --- PASO 6: VECTOR STORE ---
# 7.1. Funcion para crear la base vectorial desde los fragmentos.
def build_vector_store(chunks):
    # Obtiene el modelo que convierte texto en vectores.
    embedding_model = ollama_embedding()
    # Crea la base vectorial con los trozos del documento.
    vector_store = Chroma.from_documents(
        # Guarda los trozos ya preparados.
        documents=chunks,
        # Usa el modelo que genera vectores.
        embedding=embedding_model,
        # Asigna un nombre interno a la coleccion.
        collection_name="rag_pdf_qa_bot",
    )

    # Devuelve la base vectorial lista para retrieval.
    return vector_store

# --- PASO 7: RETRIEVER ---
# 8.1. Funcion para crear el retriever desde la base vectorial.
def build_retriever(vector_store):
    # Crea el buscador a partir de la base vectorial.
    retriever_obj = vector_store.as_retriever(
        # Busca por similitud de significado.
        search_type="similarity",
        # Limita la cantidad de resultados recuperados.
        search_kwargs={"k": TOP_K},
    )

    # Devuelve el retriever ya preparado.
    return retriever_obj

# --- PASO 8: INDEXACION ---
# 9.1. Funcion para indexar un PDF y reutilizar su retriever.
def get_rag_retriever(file_path: str):
    # Reutiliza el retriever si el PDF no ha cambiado.
    global _indexed_pdf_path
    global _rag_retriever
    global _vector_store

    # Reindexa solo si cambia el archivo o si no existe el retriever.
    if _indexed_pdf_path != file_path or _rag_retriever is None:
        # Prepara los trozos del PDF.
        chunks = prepare_chunks(file_path)
        # Crea la base vectorial con esos trozos.
        _vector_store = build_vector_store(chunks)
        # Crea el retriever usando la base vectorial.
        _rag_retriever = build_retriever(_vector_store)
        # Guarda la ruta del PDF ya indexado.
        _indexed_pdf_path = file_path

    # Devuelve el retriever listo para responder.
    return _rag_retriever

# --- PASO 9: QA CHAIN ---
# 10.1. Funcion para responder preguntas sobre un PDF cargado.
def rag_qa(file_path: str, query: str) -> str:
    # Valida que exista un archivo antes de ejecutar la cadena.
    if not file_path:
        return "Carga un archivo PDF."

    # Valida que exista una pregunta antes de consultar el modelo.
    if not query or not query.strip():
        return "Escribe una pregunta."

    # Obtiene el modelo que redacta la respuesta.
    llm = get_llm()
    # Obtiene el retriever del flujo RAG.
    retriever_obj = get_rag_retriever(file_path)
    # Crea la cadena que une el modelo y el buscador.
    qa = RetrievalQA.from_chain_type(
        # Usa el modelo de lenguaje para responder.
        llm=llm,
        # Inserta los trozos recuperados en una sola entrada.
        chain_type="stuff",
        # Usa el buscador para traer contexto del PDF.
        retriever=retriever_obj,
        # Evita devolver los documentos fuente al final.
        return_source_documents=False,
    )
    # Ejecuta la pregunta del usuario sobre la cadena.
    response = qa.invoke({"query": query})

    # Devuelve solo el texto final de la respuesta.
    return response["result"]

# --- INTERFAZ ---
# Crea la interfaz web de la practica.
rag_application = gr.Interface(
    # Usa la funcion principal para procesar la consulta.
    fn=rag_qa,
    # Desactiva el marcado manual de respuestas.
    flagging_mode="never",
    # Define los campos de entrada de la interfaz.
    inputs=[
        gr.File(
            # Muestra el nombre del campo para el archivo.
            label="Upload PDF File",
            # Permite subir un solo archivo.
            file_count="single",
            # Limita la subida a archivos PDF.
            file_types=[".pdf"],
            # Entrega la ruta del archivo al codigo.
            type="filepath",
        ),
        gr.Textbox(
            # Muestra el nombre del campo para la pregunta.
            label="Input Query",
            # Da dos lineas de altura al cuadro.
            lines=2,
            # Muestra un texto de ayuda dentro del cuadro.
            placeholder="Type your question here...",
        ),
    ],
    # Define el cuadro donde se mostrara la respuesta.
    outputs=gr.Textbox(label="Output"),
    # Muestra el titulo principal de la app.
    title="RAG Chatbot",
    # Explica al usuario para que sirve la interfaz.
    description=(
        "Upload a PDF document and ask any question. "
        "The chatbot will try to answer using the provided document."
    ),
)

# Ejecuta la interfaz solo si este archivo se lanza directamente.
if __name__ == "__main__":
    # Lanza la aplicacion usando el host y puerto definidos para la practica.
    rag_application.launch(server_name=SERVER_HOST, server_port=SERVER_PORT)
