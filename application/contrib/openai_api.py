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
        print("self.openai.api_key:", self.openai.api_key)
        pass

    def answer(self, question: str):
        response = self.openai.Completion.create(model="text-davinci-003",
                                                 prompt=question,
                                                 temperature=0,
                                                 max_tokens=1000)
        return response.get("choices")[0].get("text")
