# --- DEPENDENCIAS ---
# 1.    RetrievalQA: Para crear una cadena de pregunta y respuesta con retrieval.
# 2.       Modelos: Para obtener el LLM.
# 3.     Retrieval: Para obtener el retriever del flujo RAG.
from langchain.chains import RetrievalQA

from rag_models import get_llm
from rag_retrieval import get_rag_retriever

# --- QA ---
# 1.1. Funcion para responder preguntas sobre un PDF cargado.
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
