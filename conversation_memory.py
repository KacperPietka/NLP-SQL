class ChatMemory:
    def __init__(self):
        self.conversation_memory = [] ### make it a JSON file for now and then make it a PostgreSQL
    
    def reset(self):
        self.conversation_memory.clear()
    
    def add_memory(self, question, sql_query, results, interpretation):
        self.conversation_memory.append({
            "question": question,
            "sql_query": sql_query,
            "results": results,
            "interpretation": interpretation
        })
        
    def detect_mode(self, question) -> str:
        # Call the ML classifier model!
        pass