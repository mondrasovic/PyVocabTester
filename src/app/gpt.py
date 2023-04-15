from __future__ import annotations

import os

import openai


class ChatGPTAccessor:
    def __init__(self, environ_var_name: str = "OPENAI_API_KEY") -> None:
        openai.api_key = os.getenv(environ_var_name)

    def query(self, prompt: str) -> str:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return completion.choices[0].message.content
