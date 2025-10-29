import json
import os

class ChatMemory:
    def __init__(self, max_memory=5, file_path="memory.json"):
        self.max_memory = max_memory
        self.file_path = file_path
        self.conversation_memory = self.load_memory() ### make it a JSON file for now and then make it a PostgreSQL
    
    def load_memory(self):
        """Load existing memory.json or return an empty list."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def reset(self):
        """Clear in-memory and file-based history."""
        self.conversation_memory = []
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)
    
    def add_memory(self, question, sql_query, results, interpretation):
        """Adds memory to the conversation_memory and calls the save.json() function"""
        new_entry = {
            "question": question,
            "sql_query": sql_query,
            "results": results,
            "interpretation": interpretation
        }
        # Avoid duplicates
        if not self.conversation_memory or self.conversation_memory[-1] != new_entry:
            self.conversation_memory.append(new_entry)
            if len(self.conversation_memory) > self.max_memory:
                self.conversation_memory = self.conversation_memory[-self.max_memory:]
            self.save_to_json()
    def save_to_json(self):
        """Save the current memory list to disk."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_memory, f, ensure_ascii=False, indent=4)
        
    def detect_mode(self, question) -> str:
        # Call the ML classifier model!
        pass