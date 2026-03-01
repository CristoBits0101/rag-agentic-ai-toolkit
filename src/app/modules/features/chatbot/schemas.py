# --- DEPENDENCIAS ---


# Any: Es un tipo especial que puede ser cualquier cosa.
# Se utiliza cuando no se conoce de antemano el tipo de dato que se va a manejar.
# En este caso se usa para permitir que las variables en las invocaciones de LCEL puedan ser de cualquier tipo.
from typing import Any

# BaseModel: Es la clase base de Pydantic que se utiliza para definir modelos de datos.
# Field: Es una función de Pydantic que se utiliza para definir campos en los modelos de datos.
from pydantic import BaseModel, Field


# --- MODELOS DE DATOS ---


class GenerationParams(BaseModel):
    # Modelo a utilizar.
    model: str = Field(default="llama3.2:3b")

    # Máximo de tokens a generar en la respuesta.
    # 1 token ≈ 0.75 palabras en español.
    # 256 tokens ≈ 180–200 palabras aproximadamente.
    # Solo afecta a los tokens generados (no al prompt).
    max_new_tokens: int = Field(default=256, ge=1, le=4096)

    # Temperatura del modelo (0.0 a 2.0).
    # Controla la aleatoriedad / creatividad.
    #       0.0 → Muy determinista, respuestas casi idénticas.
    # 0.3 - 0.7 → Balanceado (ideal para uso técnico).
    #      1.0+ → Más creativo y variado.
    #      >1.5 → Puede generar respuestas incoherentes.
    temperature: float = Field(default=0.5, ge=0.0, le=2.0)

    # Top-p (Nucleus Sampling) (0.0 a 1.0).
    # Limita el conjunto de palabras candidatas según probabilidad acumulada.
    # Valores bajos → Más conservador y repetitivo.
    # Valores altos → Más variedad y naturalidad.
    #    0.8 - 0.95 → Suele ser un rango equilibrado.
    #           0.2 → Es bastante restrictivo.
    top_p: float = Field(default=0.2, ge=0.0, le=1.0)

    # Top-k (1 a 100+ según modelo).
    # Limita el número máximo de palabras candidatas consideradas.
    #            1  → Solo la palabra más probable (muy determinista).
    #         20-50 → Buen equilibrio entre precisión y variedad.
    # Valores altos → Más diversidad.
    #   Con top_k=1 → El modelo será muy rígido.
    top_k: int = Field(default=1, ge=1, le=200)


# --- EJERCICIO 1: PROMPT ENGINEERING ---


class PromptCompletionRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    params: GenerationParams | None = None


class PromptCompletionResponse(BaseModel):
    output: str


# --- EJERCICIO 2: CREACION DE PROMPTS PARA TAREAS ESPECIFICAS ---


class Exercise2Request(BaseModel):
    # 2.1) Ajustar parámetros para controlar el comportamiento de la respuesta.
    baseline_prompt: str = Field(default="El viento esta ")

    # 2.2) Diseñar prompts para tareas específicas con diccionario.
    task_prompts: dict[str, str] = Field(
        default_factory=lambda: {
            "sentiment": "Clasifica como Positivo o Negativo: 'La pelicula fue increible.'",
            "summary": "Resume en una frase: El cambio climatico afecta a ecosistemas, economias y salud.",
            "translation": "Traduce al espanol: 'Artificial intelligence is changing healthcare.'",
        }
    )

    # 2.3) One-Shot Prompting: Guiar la salida con un solo ejemplo mediante un diccionario.
    one_shot_prompts: dict[str, str] = Field(
        default_factory=lambda: {
            "formal_email": "Escribe un correo formal para solicitar una reunion con un cliente la proxima semana.\n\nCorreo:",
            "technical_concept": "Explica el concepto de aprendizaje automatico en terminos sencillos para un principiante.\n\nExplicacion:",
            "keyword_extraction": "Extrae las palabras clave principales del siguiente texto:\nArtificial intelligence and machine learning are rapidly transforming industries worldwide.\n\nPalabras clave:",
        }
    )

    # 2.4) Few-Shot Prompting: Guiar la salida con pocos ejemplos.
    few_shot_prompt: str = Field(
        default=(
            'Ingles: "How are you?"\n'
            'Frances: "Comment ca va?"\n'
            'Ingles: "Where is the train station?"\n'
            "Frances:"
        )
    )


class Exercise2Response(BaseModel):
    baseline: str
    task_outputs: dict[str, str]
    one_shot_outputs: dict[str, str]
    few_shot_output: str


# --- EJERCICIO 3: CREACION DE PROMPTS PARA EXPLICAR PROCESOS PASO A PASO ---


class Exercise3Request(BaseModel):
    # 3.1) Solicitar explicar un proceso.
    decision_making_prompt: str = Field(
        default="Explica el proceso de toma de decisiones paso a paso para elegir el mejor portatil para comprar."
    )

    # 3.2) Solicitar instrucciones.
    sandwich_making_prompt: str = Field(
        default="Explica paso a paso como hacer un sandwich simple."
    )

    # 3.4) Razonamiento guiado.
    reasoning_prompt: str = Field(
        default=(
            "Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. Ahora tengo 70, "
            "que edad tiene mi hermana?\n\n"
            "Proporciona tres calculos y explicaciones independientes y, a continuacion, "
            "determina el resultado mas coherente."
        )
    )


class Exercise3Response(BaseModel):
    # 3.3) Generar las respuestas para ambos prompts.
    decision_making: str
    sandwich_making: str
    reasoning: str


# --- EJERCICIO 4: LOGICA LCEL ---


class LcelInvocation(BaseModel):
    name: str = Field(..., min_length=1)
    template: str = Field(..., min_length=1)
    variables: dict[str, Any] = Field(default_factory=dict)


class Exercise4Request(BaseModel):
    # 4.2) Ejercicios con LCEL:
    # - Chistes dinámicos
    # - Resúmenes dinámicos
    # - Preguntas y respuestas dinámicas
    # - Clasificación dinámica
    # - Generación SQL dinámica
    invocations: list[LcelInvocation] = Field(
        default_factory=lambda: [
            LcelInvocation(
                name="joke",
                template="Cuentame un chiste {adjective} sobre {content}.",
                variables={"adjective": "gracioso", "content": "gallinas"},
            ),
            LcelInvocation(
                name="summary",
                template="Resume el siguiente contenido en una frase:\n{content}",
                variables={
                    "content": (
                        "El rapido avance de la tecnologia en el siglo XXI ha transformado salud, "
                        "educacion y transporte. IA y machine learning mejoran diagnosticos, "
                        "eficiencia y acceso al conocimiento."
                    )
                },
            ),
        ]
    )
    params: GenerationParams | None = None


class Exercise4Response(BaseModel):
    outputs: dict[str, str]


# --- EJERCICIO 5: RAZONAMIENTO GUIADO + ANALISIS ESTRUCTURADO EN LCEL ---


class Exercise5Request(BaseModel):
    # 5.4) Procesar multiples resenas (batch simple).
    reviews: list[str] = Field(
        default_factory=lambda: [
            "I love this smartphone! The camera quality is exceptional and the battery lasts all day.",
            "This laptop is terrible. It's slow, crashes frequently, and the keyboard stopped working.",
        ],
        min_length=1,
    )

    # 5.5) Prompt de razonamiento paso a paso con formato de salida.
    problem: str = Field(
        default=(
            "Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. "
            "Ahora tengo 70. Cuantos anos tiene mi hermana?"
        )
    )


class Exercise5Response(BaseModel):
    review_analysis: list[str]
    reasoning: str
