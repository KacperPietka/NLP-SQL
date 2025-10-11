import json
import requests


class NLToSQLModel:
    def __init__(self, question, schema, context):
        self.schema = schema
        self.context = context
        self.question = question
        self.full_prompt = f"""
        You are an expert SQL query generator. Generate a SQL query based strictly on the schema and context provided below.

        Schema:
        {self.schema}

        Context:
        {self.context}

        User Question:
        {self.question}

        Rules:
        - Only use the tables and columns in the schema.
        - Never invent new tables or columns.
        - Return only the SQL query — no explanations or text.

        SQL:
        """
        self.payload = {
            "model": "hf.co/defog/sqlcoder-7b-2:Q5_K_M",
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