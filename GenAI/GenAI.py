from ollama import Client

class LLM_connect:
    def __init__(self, model='smollm2', port=11434):
        self.model = model
        self.host = f'http://localhost:{port}'
        self.client = Client(
            host=self.host,
            headers={'x-some-header': 'some-value'}
        )

    def chat(self, data):
        response = self.client.chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': data
            }
        ])
        
        answer = response['message']['content']
        return answer

if __name__ == '__main__':
    c = LLM_connect()
    while True:
        data = input('Ask : ')
        print(c.chat(data))