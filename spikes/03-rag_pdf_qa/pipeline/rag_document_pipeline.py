# --- DEPENDENCIAS ---
# 1.   TextSplitter: Para dividir el contenido del PDF en fragmentos manejables.
# 2.    PyPDFLoader: Para cargar el contenido del PDF como documentos LangChain.
# 3.   Configuracion: Para leer tamano y solape de los trozos.
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from config.rag_config import CHUNK_OVERLAP
from config.rag_config import CHUNK_SIZE

# --- DOCUMENTOS ---
# 1.1. Funcion para cargar un PDF como documentos LangChain.
def load_pdf_documents(file_path: str):
    # Crea una instancia de PyPDFLoader con el archivo preparado.
    loader = PyPDFLoader(file_path)
    # Lee el contenido del archivo y lo convierte en una lista de documentos con texto y metadatos.
    loaded_documents = loader.load()

    # Devuelve el documento completo cargado desde PDF.
    return loaded_documents


# 1.2. Funcion para partir los documentos en trozos.
def split_loaded_documents(loaded_documents):
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
    chunks = splitter.split_documents(loaded_documents)

    # Devuelve los trozos generados.
    return chunks


# 1.3. Funcion para preparar los trozos del PDF.
def prepare_pdf_chunks(file_path: str):
    # Carga el PDF y obtiene sus documentos.
    loaded_documents = load_pdf_documents(file_path)
    # Parte esos documentos en trozos pequenos.
    chunks = split_loaded_documents(loaded_documents)

    # Devuelve los trozos listos para indexar.
    return chunks
