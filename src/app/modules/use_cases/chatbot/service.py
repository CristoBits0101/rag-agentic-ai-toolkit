from __future__ import annotations

from typing import Any

from app.modules.components.agents.prompts import templates
from app.modules.use_cases.chatbot.schemas import (
    Exercise2Request,
    Exercise3Request,
    Exercise4Request,
    Exercise5Request,
    GenerationParams,
    PromptCompletionRequest,
)

# --- LEYENDA ---
# 1.        LangChain: Prompts • Memory • Chains • Agents • Tools • RAG • LLMs
# 2.   LangChain Core: PromptTemplate • Runnable/LCEL • ChatModel/LLM • OutputParser
# 3. LangChain Ollama: llama3.1:latest • mistral:latest • phi3.5:latest

# --- INSTALACIÓN ---
# 1.           Ollama: irm https://ollama.com/install.ps1 | iex
# 2.  LLM llama3.2:3b: ollama pull llama3.2:3b
# 3.       LangChain*: pip install -U langchain langchain-core langchain-ollama
# 4. LangChain Ollama: pip install -U langchain-ollama

# --- VERIFICACIÓN ---
# 1.           Ollama: ollama --version
# 2.  Ollama Servidor: ollama serve
# 3.        LangChain: pip show langchain
# 4.   Ollama Modelos: ollama list

# --- DEPENDENCIAS ---
# 1.        OllamaLLM: Para interactuar con modelos Ollama desde LangChain.
# 2.   PromptTemplate: Para crear plantillas de prompts con variables dinámicas.


class PromptService:
    # --- EJERCICIO 1: PROMPT ENGINEERING ---

    # 1.1) Función para cargar el modelo:
    # @params: prompt_txt: Texto del prompt.
    # @params: params: Diccionario de parámetros.
    # @return: Respuesta del modelo.
    @staticmethod
    def _resolve_params(
        params: GenerationParams | None,
        *,
        defaults: dict[str, Any] | None = None,
    ) -> GenerationParams:
        # Parámetros por defecto.
        base = GenerationParams().model_dump()

        # Actualiza los parámetros por defecto con los parámetros proporcionados.
        # None no es un diccionario, por lo que no se puede actualizar.
        if defaults:
            base.update(defaults)
        if params:
            base.update(params.model_dump())

        return GenerationParams(**base)

    @staticmethod
    def _invoke_llm(prompt_txt: str, params: GenerationParams) -> str:
        try:
            from langchain_ollama import OllamaLLM
        except ImportError as exc:
            raise RuntimeError(
                "Missing dependency: install langchain, langchain-core and langchain-ollama."
            ) from exc

        # Inicializa el modelo Ollama.
        llm = OllamaLLM(
            # Modelo a utilizar.
            model=params.model,
            # Temperatura del modelo.
            temperature=params.temperature,
            # Top-p del modelo.
            top_p=params.top_p,
            # Top-k del modelo.
            top_k=params.top_k,
            # Máximo de tokens a generar en la respuesta.
            num_predict=params.max_new_tokens,
        )

        return llm.invoke(prompt_txt)

    # 1.2) Imprime la respuesta del modelo.
    # En versión API retorna la respuesta para que el router construya el JSON.
    def run_exercise_1(self, payload: PromptCompletionRequest) -> str:
        params = self._resolve_params(payload.params)
        return self._invoke_llm(payload.prompt, params)

    # --- EJERCICIO 2: CREACION DE PROMPTS PARA TAREAS ESPECIFICAS ---

    # 2.1) Ajustar parámetros para controlar el comportamiento de la respuesta.
    # 2.2) Diseñar prompts para tareas específicas con diccionario.
    # 2.3) One-Shot Prompting: Guiar la salida con un solo ejemplo.
    # 2.4) Few-Shot Prompting: Guiar la salida con pocos ejemplos.
    def run_exercise_2(self, payload: Exercise2Request) -> dict[str, Any]:
        # 2.1) Ajustar parámetros para controlar el comportamiento de la respuesta.
        baseline_params = self._resolve_params(
            None,
            defaults={
                "max_new_tokens": 128,
                "temperature": 0.5,
                "top_p": 0.2,
                "top_k": 1,
            },
        )

        # Modificar los parámetros para mejorar la respuesta.
        task_params = self._resolve_params(
            None,
            defaults={
                "max_new_tokens": 120,
                "temperature": 0.3,
                "top_p": 0.9,
                "top_k": 40,
            },
        )

        # 2.4) Few-Shot Prompting: Guiar la salida con pocos ejemplos.
        few_shot_params = self._resolve_params(
            None,
            defaults={
                "max_new_tokens": 60,
                "temperature": 0.1,
                "top_p": 0.9,
                "top_k": 40,
            },
        )

        baseline = self._invoke_llm(payload.baseline_prompt, baseline_params)

        # 2.2) Diseñar prompts para tareas específicas con diccionario.
        # Definir los prompts (vienen en payload.task_prompts).
        # Iterar sobre los prompts y generar las respuestas.
        task_outputs = {
            name: self._invoke_llm(prompt, task_params)
            for name, prompt in payload.task_prompts.items()
        }

        # 2.3) One-Shot Prompting: Guiar la salida con un solo ejemplo mediante un diccionario.
        one_shot_outputs = {
            name: self._invoke_llm(prompt, task_params)
            for name, prompt in payload.one_shot_prompts.items()
        }

        # 2.4) Few-Shot Prompting.
        few_shot_output = self._invoke_llm(payload.few_shot_prompt, few_shot_params)

        return {
            "baseline": baseline,
            "task_outputs": task_outputs,
            "one_shot_outputs": one_shot_outputs,
            "few_shot_output": few_shot_output,
        }

    # --- EJERCICIO 3: CREACION DE PROMPTS PARA EXPLICAR PROCESOS PASO A PASO ---

    # 3.1) Solicitar explicar un proceso.
    # 3.2) Solicitar instrucciones.
    # 3.3) Generar las respuestas para ambos prompts.
    # 3.4) Razonamiento guiado con salida más extensa.
    def run_exercise_3(self, payload: Exercise3Request) -> dict[str, str]:
        step_params = self._resolve_params(
            None,
            defaults={
                "max_new_tokens": 220,
                "temperature": 0.3,
                "top_p": 0.9,
                "top_k": 40,
            },
        )

        # 3.4) Razonamiento guiado.
        # Aumentamos el max_new_tokens para permitir respuestas más largas y detalladas.
        reasoning_params = self._resolve_params(
            None,
            defaults={
                "max_new_tokens": 512,
                "temperature": 0.2,
                "top_p": 0.9,
                "top_k": 40,
            },
        )

        # 3.3) Generar las respuestas para ambos prompts.
        responses = {
            "decision_making": self._invoke_llm(payload.decision_making_prompt, step_params),
            "sandwich_making": self._invoke_llm(payload.sandwich_making_prompt, step_params),
        }

        # Generar la respuesta para el prompt de razonamiento guiado.
        responses["reasoning"] = self._invoke_llm(payload.reasoning_prompt, reasoning_params)

        return responses

    # --- EJERCICIO 4: LOGICA LCEL ---

    # 4.1) Función para construir un chain LCEL con PromptTemplate y OllamaLLM:
    # @params: prompt_template: Texto del template con variables entre llaves {variable}.
    # @return: Chain de LCEL que puede ser invocado con invoke().
    # 4.2) Ejercicios con LCEL:
    # - Chistes dinámicos
    # - Resúmenes dinámicos
    # - Preguntas y respuestas dinámicas
    # - Clasificación dinámica
    # - Generación SQL dinámica
    def run_exercise_4(self, payload: Exercise4Request) -> dict[str, str]:
        params = self._resolve_params(
            payload.params,
            defaults={"temperature": 0.3, "top_p": 0.9, "top_k": 40},
        )

        try:
            from langchain_core.prompts import PromptTemplate
            from langchain_ollama import OllamaLLM
        except ImportError as exc:
            raise RuntimeError(
                "Missing dependency: install langchain, langchain-core and langchain-ollama."
            ) from exc

        # Inicializa el modelo Ollama con parámetros por defecto.
        llm = OllamaLLM(
            model=params.model,
            temperature=params.temperature,
            top_p=params.top_p,
            top_k=params.top_k,
            num_predict=params.max_new_tokens,
        )

        outputs: dict[str, str] = {}
        for invocation in payload.invocations:
            # Crea un PromptTemplate a partir de un texto con variables dinámicas entre llaves {}.
            prompt = PromptTemplate.from_template(invocation.template)

            # En LangChain "LCEL" significa que todo componente ejecutable es un Runnable.
            # Un Runnable es un objeto que implementa .invoke(), recibe una entrada y devuelve una salida.
            # Construimos un Runnable Chain usando LCEL con el operador | (pipe) se encadena Runnables.
            chain = prompt | llm

            # Se puede invocar el chain con invoke() pasando un diccionario con los valores de las variables.
            outputs[invocation.name] = chain.invoke(invocation.variables)

        return outputs

    # --- EJERCICIO 5: RAZONAMIENTO GUIADO + ANALISIS ESTRUCTURADO EN LCEL ---

    # 5.1) LLM dedicado para este ejercicio con salida más extensa.
    # 5.2) Plantilla para analizar reseñas con formato fijo.
    # 5.3) Formateador explícito + parser de texto para cadena LCEL completa.
    # 5.4) Procesar multiples reseñas (batch simple).
    # 5.5) Prompt de razonamiento paso a paso con formato de salida.
    def run_exercise_5(self, payload: Exercise5Request) -> dict[str, Any]:
        params = self._resolve_params(
            None,
            defaults={
                "max_new_tokens": 512,
                "temperature": 0.2,
                "top_p": 0.9,
                "top_k": 40,
            },
        )

        try:
            from langchain_core.output_parsers import StrOutputParser
            from langchain_core.prompts import PromptTemplate
            from langchain_core.runnables import RunnableLambda
            from langchain_ollama import OllamaLLM
        except ImportError as exc:
            raise RuntimeError(
                "Missing dependency: install langchain, langchain-core and langchain-ollama."
            ) from exc

        llm = OllamaLLM(
            model=params.model,
            temperature=params.temperature,
            top_p=params.top_p,
            top_k=params.top_k,
            num_predict=params.max_new_tokens,
        )

        # 5.2) Plantilla para analizar reseñas con formato fijo.
        review_prompt = PromptTemplate.from_template(templates.DEFAULT_REVIEW_TEMPLATE)
        reasoning_prompt = PromptTemplate.from_template(templates.DEFAULT_REASONING_TEMPLATE)

        # 5.3) Formateador explícito + parser de texto para cadena LCEL completa.
        review_chain = (
            RunnableLambda(lambda variables: review_prompt.format(**variables))
            | llm
            | StrOutputParser()
        )
        reasoning_chain = (
            RunnableLambda(lambda variables: reasoning_prompt.format(**variables))
            | llm
            | StrOutputParser()
        )

        # 5.4) Procesar multiples reseñas (batch simple).
        review_analysis = [
            review_chain.invoke({"review": review}) for review in payload.reviews
        ]

        # 5.5) Prompt de razonamiento paso a paso con formato de salida.
        reasoning = reasoning_chain.invoke({"problem": payload.problem})

        return {"review_analysis": review_analysis, "reasoning": reasoning}


prompt_service = PromptService()
