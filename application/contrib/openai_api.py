import copy
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
            messages = copy.deepcopy(context)
            messages.append(message)
        else:
            messages = [message]
        response = self.openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                     messages=messages,
                                                     temperature=0,
                                                     max_tokens=3000)
        # print(response)
        return response.get("choices")[0].get("message").get("content")
