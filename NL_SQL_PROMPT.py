PROMPT = f"""
        ROLE: You are a SQL expert.
        TASK: Using the following schema context, generate a SQL query based on the question.

        Schema:
        {context}

        Question:
        {question}
        """
