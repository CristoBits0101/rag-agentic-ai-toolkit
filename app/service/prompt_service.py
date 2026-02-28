from __future__ import annotations

from typing import Any

from app.api.v1.prompt import prompt_engineering_templates as templates
from app.schemas.prompt_schemas import (
    Exercise2Request,
    Exercise3Request,
    Exercise4Request,
    Exercise5Request,
    GenerationParams,
    PromptCompletionRequest,
)


class PromptService:
    @staticmethod
    def _resolve_params(
        params: GenerationParams | None,
        *,
        defaults: dict[str, Any] | None = None,
    ) -> GenerationParams:
        base = GenerationParams().model_dump()
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

        llm = OllamaLLM(
            model=params.model,
            temperature=params.temperature,
            top_p=params.top_p,
            top_k=params.top_k,
            num_predict=params.max_new_tokens,
        )
        return llm.invoke(prompt_txt)

    def run_exercise_1(self, payload: PromptCompletionRequest) -> str:
        params = self._resolve_params(payload.params)
        return self._invoke_llm(payload.prompt, params)

    def run_exercise_2(self, payload: Exercise2Request) -> dict[str, Any]:
        baseline_params = self._resolve_params(
            None,
            defaults={
                "max_new_tokens": 128,
                "temperature": 0.5,
                "top_p": 0.2,
                "top_k": 1,
            },
        )
        task_params = self._resolve_params(
            None,
            defaults={
                "max_new_tokens": 120,
                "temperature": 0.3,
                "top_p": 0.9,
                "top_k": 40,
            },
        )
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

        task_outputs = {
            name: self._invoke_llm(prompt, task_params)
            for name, prompt in payload.task_prompts.items()
        }
        one_shot_outputs = {
            name: self._invoke_llm(prompt, task_params)
            for name, prompt in payload.one_shot_prompts.items()
        }
        few_shot_output = self._invoke_llm(payload.few_shot_prompt, few_shot_params)

        return {
            "baseline": baseline,
            "task_outputs": task_outputs,
            "one_shot_outputs": one_shot_outputs,
            "few_shot_output": few_shot_output,
        }

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
        reasoning_params = self._resolve_params(
            None,
            defaults={
                "max_new_tokens": 512,
                "temperature": 0.2,
                "top_p": 0.9,
                "top_k": 40,
            },
        )

        return {
            "decision_making": self._invoke_llm(
                payload.decision_making_prompt, step_params
            ),
            "sandwich_making": self._invoke_llm(
                payload.sandwich_making_prompt, step_params
            ),
            "reasoning": self._invoke_llm(payload.reasoning_prompt, reasoning_params),
        }

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

        llm = OllamaLLM(
            model=params.model,
            temperature=params.temperature,
            top_p=params.top_p,
            top_k=params.top_k,
            num_predict=params.max_new_tokens,
        )

        outputs: dict[str, str] = {}
        for invocation in payload.invocations:
            prompt = PromptTemplate.from_template(invocation.template)
            chain = prompt | llm
            outputs[invocation.name] = chain.invoke(invocation.variables)

        return outputs

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

        review_prompt = PromptTemplate.from_template(templates.DEFAULT_REVIEW_TEMPLATE)
        reasoning_prompt = PromptTemplate.from_template(
            templates.DEFAULT_REASONING_TEMPLATE
        )

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

        review_analysis = [
            review_chain.invoke({"review": review}) for review in payload.reviews
        ]
        reasoning = reasoning_chain.invoke({"problem": payload.problem})

        return {"review_analysis": review_analysis, "reasoning": reasoning}


prompt_service = PromptService()
