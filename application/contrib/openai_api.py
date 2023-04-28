import copy
import time
from typing import List

import openai


class OpenAI:

    def __init__(self, app=None):
        self.openai = openai
        self.app = app
        if self.app:
            self.init_app(app)
        pass

    def init_app(self, app):
        self.openai.api_key = app.config.get("OPENAI_KEY")
        pass

    def answer(self, question: str, context: List[dict] = None):
        message = {"role": "user",
                   "content": question}
        if context:
            messages = []
            for m in context:
                t = m.pop("t", 0)
                if t > time.time() - 5 * 60:
                    messages.append(m)
            messages.append(message)
        else:
            messages = [message]

        max_tokens = 4096 - len("".join([m.get("content") for m in messages])) * 2

        response = self.openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                     messages=messages,
                                                     temperature=0,
                                                     max_tokens=max_tokens)
        # print(response)
        return response.get("choices")[0].get("message").get("content")
