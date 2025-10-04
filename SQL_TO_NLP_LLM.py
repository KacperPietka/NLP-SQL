import requests

class NLToSQLModel:
    def __init__(self, question, results):
        self.question = question
        self.results = results
        self.full_prompt = f"""
        Your role is to explain the generated query based on the user question.

        User Question:
        {self.question}

        SQL:
        {self.results}


        Rules:
        - Return only the explanation — no SQL or additional text.
        - Keep it concise and clear.

        """
        self.payload = {
            "model": "mistral",
            "prompt": self.full_prompt,
            "stream": False 
        }
    def run(self):
        response = requests.post("http://localhost:11434/api/generate", json=self.payload)
        if response.status_code == 200:
            data = response.json()
            return data["response"].strip()
        else:
            raise Exception(f"Ollama API error: {response.text}")