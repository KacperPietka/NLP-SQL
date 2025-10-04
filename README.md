# NLP-SQL

# Natural Language to SQL with Local LLMs  

**SQL-NLP** lets you ask questions in plain English and get accurate SQL queries — powered by **Ollama** and the **SQLCoder-7B-2** model.  
The system retrieves relevant database schema information from **ChromaDB** and generates correct SQL that can be executed on your local database.  

## 🚀 Features  

- Ask natural-language questions → get executable SQL 
- Schema-aware SQL generation using Chroma vector search  
- ChatGPT-style desktop GUI built with PyQt 6  
- SQLite / dbt-style schema integration

## 🧠 Workflow  

The **SQL-NLP** system transforms a natural language question into a fully executable SQL query through four key stages:
---
### Schema Embedding  
- The database schema (from `.yml` or `.sql` files) is **embedded** into a **Chroma vector database**.  
- Each **table**, **column**, and **relationship** description is converted into a vector representation using text embeddings.  
- This makes the schema **searchable semantically** — the system can find the most relevant parts of the schema for any question.  
---
### Schema Retrieval  
- When a user asks a question (e.g., *"Which vendor had the highest performance in 2024?"*),  
  the query text is converted into an embedding vector.  
- Chroma performs a **similarity search** to find the most relevant schema fragments.  
- These retrieved tables and columns form the **context** for SQL generation.  
---
### SQL Generation  
- The retrieved schema context and user question are inserted into a **prompt template**. 
- This full prompt is then sent to the **SQLCoder-7B-2 model** running locally via **Ollama**.  
- The model generates a **syntactically correct SQL query**, following strict rules:
  - Use only existing tables and columns  
  - Prefer explicit JOINs  
  - No commentary, just clean SQL 
---
### Execute SQL
- The generated SQL query is executed on the local SQLite (or any configured) database.
- Execution can be handled through the SQL_EXECUTE.py module.
- The resulting data is returned as a structured dataset (rows and columns).
---
### Translate Results Back to Natural Language
- The results from SQL execution are passed to the SQL → NLP model (optional module: SQL_TO_NLP_LLM.py).
- The model summarizes or explains the output in plain language for the user.
- ***Example: *** “The vendor with the highest performance in 2024 is Acme Corp, with a score of 97.”
