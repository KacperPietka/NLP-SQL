from embedding_schema import ChromaSchemaManager

manager = ChromaSchemaManager()
manager.add_yml("yml_files/example_schema.yml")
print("✅ finished adding")
