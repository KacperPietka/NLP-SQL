import requests

class SQLResultExplainer:
    def __init__(self, question, sql_query, results, schema=None, context=None):
        self.question = question
        self.sql_query = sql_query
        self.results = results
        self.schema = schema
        self.context = context

        self.full_prompt = f"""
        You are an expert data analyst. Explain the **results** of the SQL query below,
        based on the question asked by the user.

        User Question:
        {self.question}

        SQL Query:
        {self.sql_query}

        Results (JSON):
        {self.results}

        Schema:
        {self.schema}

        Context:
        {self.context}

        Rules:
        - Focus on interpreting the *results* (trends, comparisons, insights).
        - Avoid restating the SQL or technical details.
        - Keep it clear, concise, and human-readable.
        - Don't write "based on your query" etc.
        """
        self.payload = {
            "model": "mistral",
            "prompt": self.full_prompt,
            "stream": False
        }

    def run(self):
        response = requests.post("http://localhost:11434/api/generate", json=self.payload)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            raise Exception(f"Ollama API error: {response.text}")
