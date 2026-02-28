from typing import Any

from pydantic import BaseModel, Field


class GenerationParams(BaseModel):
    model: str = Field(default="llama3.2:3b")
    max_new_tokens: int = Field(default=256, ge=1, le=4096)
    temperature: float = Field(default=0.5, ge=0.0, le=2.0)
    top_p: float = Field(default=0.2, ge=0.0, le=1.0)
    top_k: int = Field(default=1, ge=1, le=200)


class PromptCompletionRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    params: GenerationParams | None = None


class PromptCompletionResponse(BaseModel):
    output: str


class Exercise2Request(BaseModel):
    baseline_prompt: str = Field(default="El viento esta ")
    task_prompts: dict[str, str] = Field(
        default_factory=lambda: {
            "sentiment": "Clasifica como Positivo o Negativo: 'La pelicula fue increible.'",
            "summary": "Resume en una frase: El cambio climatico afecta a ecosistemas, economias y salud.",
            "translation": "Traduce al espanol: 'Artificial intelligence is changing healthcare.'",
        }
    )
    one_shot_prompts: dict[str, str] = Field(
        default_factory=lambda: {
            "formal_email": "Escribe un correo formal para solicitar una reunion con un cliente la proxima semana.\n\nCorreo:",
            "technical_concept": "Explica el concepto de aprendizaje automatico en terminos sencillos para un principiante.\n\nExplicacion:",
            "keyword_extraction": "Extrae las palabras clave principales del siguiente texto:\nArtificial intelligence and machine learning are rapidly transforming industries worldwide.\n\nPalabras clave:",
        }
    )
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


class Exercise3Request(BaseModel):
    decision_making_prompt: str = Field(
        default="Explica el proceso de toma de decisiones paso a paso para elegir el mejor portatil para comprar."
    )
    sandwich_making_prompt: str = Field(
        default="Explica paso a paso como hacer un sandwich simple."
    )
    reasoning_prompt: str = Field(
        default=(
            "Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. Ahora tengo 70, "
            "que edad tiene mi hermana?\n\n"
            "Proporciona tres calculos y explicaciones independientes y, a continuacion, "
            "determina el resultado mas coherente."
        )
    )


class Exercise3Response(BaseModel):
    decision_making: str
    sandwich_making: str
    reasoning: str


class LcelInvocation(BaseModel):
    name: str = Field(..., min_length=1)
    template: str = Field(..., min_length=1)
    variables: dict[str, Any] = Field(default_factory=dict)


class Exercise4Request(BaseModel):
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


class Exercise5Request(BaseModel):
    reviews: list[str] = Field(
        default_factory=lambda: [
            "I love this smartphone! The camera quality is exceptional and the battery lasts all day.",
            "This laptop is terrible. It's slow, crashes frequently, and the keyboard stopped working.",
        ],
        min_length=1,
    )
    problem: str = Field(
        default=(
            "Cuando tenia 6 anos, mi hermana tenia la mitad de mi edad. "
            "Ahora tengo 70. Cuantos anos tiene mi hermana?"
        )
    )


class Exercise5Response(BaseModel):
    review_analysis: list[str]
    reasoning: str
