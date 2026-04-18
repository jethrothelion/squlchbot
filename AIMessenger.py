import ollama

class AIMessenger:
    context = []


    @classmethod
    def add_message(self, role, message):
        self.context.append({'role':role, 'content':message})

    @classmethod
    def generate(self):
        response = ollama.chat(
            model='qwen3.5:9b',
            messages=[{'role': 'user', 'content': self.context}]
        )

        reply = response['message']['content']

        self.add_message('assistant', reply)
        return reply


    @classmethod
    def clear_context(self):
        self.context = []