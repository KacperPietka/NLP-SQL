import json
import requests

from NL_SQL_PROMPT import PROMPT

class NLToSQLModel:
    def __init__(self, question, schema):
        self.schema = schema
        self.question = question
        self.full_prompt = f"""
        You are an expert SQL query generator. Generate a SQL query based strictly on the schema provided below.

        Schema:
        {self.schema}

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
        
if __name__ == "__main__":
    schema = """
    Table vendors(id, name, performance_score, year)
    Table sales(id, vendor_id, amount, date)
    """
    question = "Which vendor had the highest performance in 2024?"

    model = NLToSQLModel(question, schema)
    sql_query = model.run()
    print("Generated SQL:", sql_query)