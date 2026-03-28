# --- DEPENDENCIAS ---
# 1. StrOutputParser: Para normalizar la salida del modelo a texto.
# 2. PromptTemplate: Para construir prompts reutilizables.
# 3. Configuracion: Para leer prompts y consultas base.
# 4. Modelos: Para crear el LLM local.
# 5. Retrieval: Para recuperar contexto relevante del perfil.
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from config.icebreaker_config import FACT_QUERY
from config.icebreaker_config import INITIAL_FACTS_TEMPLATE
from config.icebreaker_config import USER_QUESTION_TEMPLATE
from models.icebreaker_models import build_llm
from orchestration.icebreaker_orchestration_retrieval import get_profile_retriever

# --- QA ---
# 1.1. Funcion para recuperar el contexto mas relevante de un perfil.
def build_context(profile_key: str, query: str) -> str:
    # Obtiene el retriever ya indexado para el perfil activo.
    retriever_obj = get_profile_retriever(profile_key)
    # Recupera los trozos mas cercanos a la consulta.
    documents = retriever_obj.invoke(query)

    # Une el texto recuperado en un bloque que pueda leer el modelo.
    return "\n\n".join(document.page_content for document in documents)


# 1.2. Funcion para ejecutar un prompt sobre contexto recuperado.
def run_prompt(
    prompt_template: str,
    context_str: str,
    model_name: str,
    temperature: float,
    num_predict: int,
    query_str: str | None = None,
) -> str:
    # Devuelve una respuesta segura si no hubo contexto suficiente.
    if not context_str.strip():
        return "I do not know."

    # Crea el prompt y el modelo para esta llamada concreta.
    prompt = PromptTemplate.from_template(prompt_template)
    llm = build_llm(
        model_name=model_name,
        temperature=temperature,
        num_predict=num_predict,
    )
    parser = StrOutputParser()
    chain = prompt | llm | parser
    payload = {"context_str": context_str}

    # Incluye la pregunta solo cuando el prompt la necesita.
    if query_str is not None:
        payload["query_str"] = query_str

    # Ejecuta la cadena y limpia espacios al final.
    return chain.invoke(payload).strip()


# 1.3. Funcion para generar tres hechos iniciales del perfil.
def generate_initial_facts(profile_key: str, model_name: str) -> str:
    # Construye contexto usando una consulta fija orientada a icebreakers.
    context_str = build_context(profile_key, FACT_QUERY)

    # Devuelve la salida del modelo con formato enumerado.
    return run_prompt(
        INITIAL_FACTS_TEMPLATE,
        context_str,
        model_name,
        temperature=0.1,
        num_predict=384,
    )


# 1.4. Funcion para responder una pregunta del usuario sobre el perfil.
def answer_user_query(profile_key: str, user_query: str, model_name: str) -> str:
    # Exige una pregunta real antes de consultar el retriever.
    if not user_query or not user_query.strip():
        return "Escribe una pregunta."

    # Recupera contexto alineado con la pregunta enviada.
    context_str = build_context(profile_key, user_query)

    # Devuelve una respuesta factual basada solo en el contexto.
    return run_prompt(
        USER_QUESTION_TEMPLATE,
        context_str,
        model_name,
        temperature=0.0,
        num_predict=256,
        query_str=user_query,
    )
