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

        base_url = settings.llm_base_url or 'https://api.openai.com/v1'
        api_key = settings.effective_llm_api_key
        model = settings.effective_llm_model
        if not api_key or not model:
            raise ValueError('LLM_MODE is openai_compatible but configuration is missing.')

        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        payload = {'model': model, 'messages': [{'role': 'user', 'content': grounded_answer_prompt(question, context)}]}
        response = httpx.post(
            f'{base_url}/chat/completions',
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
