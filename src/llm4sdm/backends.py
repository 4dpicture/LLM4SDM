import re
from typing import Type, TypeVar

from ollama import Client, Options
from openai import OpenAI
from pydantic import BaseModel

from .structured_output import SDMAssessmentResponse

R = TypeVar("R", bound=BaseModel)

_FENCE_RE = re.compile(
    r"^\s*```(?:json)?\s*(?P<body>.*?)\s*```\s*\Z",
    re.DOTALL | re.IGNORECASE,
)


def _strip_json_fence(content: str) -> str:
    """Return JSON body unwrapped from a ```json ... ``` markdown fence.

    Guided decoding should make fences impossible, but some backends silently
    fall back to unconstrained generation; this keeps the client robust."""
    m = _FENCE_RE.match(content)
    return m.group("body") if m else content.strip()


class VLLMBackend:
    def __init__(
        self,
        model_name: str,
        base_url: str = "http://localhost:8000/v1",
        api_key: str = "EMPTY",
        options: dict | None = None,
    ):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model_name
        self.options = options or {}

    def generate(
        self,
        prompt: str,
        response_model: Type[R] = SDMAssessmentResponse,
    ) -> R:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.options.get("temperature", 0.0),
            top_p=self.options.get("top_p", 0.9),
            max_tokens=self.options.get("max_new_tokens", 4096),
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__,
                    "schema": response_model.model_json_schema(),
                    "strict": True,
                },
            },
            extra_body={
                "top_k": self.options.get("top_k", 40),
                "repetition_penalty": self.options.get(
                    "repetition_penalty", 1.0
                ),
            },
        )
        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("vLLM returned empty completion content")
        return response_model.model_validate_json(_strip_json_fence(content))


class OllamaBackend:
    def __init__(
        self,
        model_name: str,
        base_url: str = "http://localhost:11434",
        options: dict | None = None,
    ):
        self.client = Client(base_url=base_url)
        options = options or {}
        self.options = Options(
            num_ctx=options.get("num_ctx", 32768),
            repeat_penalty=options.get("repeat_penalty", 1.03),
            temperature=options.get("temperature", 0.0),
            top_k=options.get("top_k", 40),
            top_p=options.get("top_p", 0.9),
        )
        self.model_name = model_name

    def generate(
        self,
        prompt: str,
        response_model: Type[R] = SDMAssessmentResponse,
    ) -> R:
        response = self.client.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            options=self.options,
            format=response_model.model_json_schema(),
        )
        content = response.message.content
        if content is None:
            raise RuntimeError("Ollama returned empty completion content")
        return response_model.model_validate_json(_strip_json_fence(content))


class BackendFactory:
    @staticmethod
    def create_backend(provider: str, provider_config: dict):
        if provider == "ollama":
            return OllamaBackend(
                model_name=provider_config["model_name"],
                base_url=provider_config.get(
                    "base_url", "http://localhost:11434"
                ),
                options=provider_config.get("options", {}),
            )
        elif provider == "vllm":
            return VLLMBackend(
                model_name=provider_config["model_name"],
                base_url=provider_config.get(
                    "base_url", "http://localhost:8000/v1"
                ),
                api_key=provider_config.get("api_key", "EMPTY"),
                options=provider_config.get("options", {}),
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")
