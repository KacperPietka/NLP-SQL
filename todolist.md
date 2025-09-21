https://huggingface.co/defog/sqlcoder-7b-2 --> Use this model for NLP --> SQL

1. Put all your database schemas, table definitions, column descriptions, and business docs into a vector DB Chroma LOCALLY!
https://docs.trychroma.com/docs/overview/getting-started

Retrieve schema + relevant docs from vector DB.

Feed that into SQLCoder’s prompt.

SQLCoder generates correct query.

Run query against your DB and return result.

dbt stores your data models as SQL files (.sql) with schema.yml files describing columns, docs, relationships, etc.

You add a new model vendor_performance.sql in dbt.

Add vendor_performance.yml with column docs.

Run dbt run && dbt docs generate.


Automation script:


Reads new schema info → updates embeddings in Chroma.


Next time someone asks “Which vendor had the highest performance in 2024?” →


Chroma retrieves the vendor_performance schema.


SQLCoder uses it to generate the correct query.
Reads dbt manifest.json / yml files


Embeds schema descriptions


Stores them in Chroma for retrieval?
