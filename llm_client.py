from __future__ import annotations

import os
from typing import Any

import httpx

from prompts import grounded_answer_prompt, mock_answer
from settings import settings


class LLMClient:
    def __init__(self, mode: str | None = None):
        self.mode = mode or settings.llm_mode
        if self.mode not in {'mock', 'openai_compatible'}:
            raise ValueError(f'Unsupported LLM mode: {self.mode}')

    def generate(self, question: str, context: str) -> str:
        if self.mode == 'mock':
            return mock_answer(question, context)
        prompt = grounded_answer_prompt(question, context)
        if not settings.llm_base_url or not settings.llm_model or not settings.llm_api_key:
            raise ValueError('LLM_MODE is openai_compatible but configuration is missing.')
        headers = {'Authorization': f'Bearer {settings.llm_api_key}', 'Content-Type': 'application/json'}
        payload = {'model': settings.llm_model, 'messages': [{'role': 'user', 'content': prompt}]}
        response = httpx.post(
            f'{settings.llm_base_url}/chat/completions',
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        body = response.json()
        return body['choices'][0]['message']['content']

    @property
    def mode_label(self) -> str:
        return 'mock' if self.mode == 'mock' else 'openai_compatible'
