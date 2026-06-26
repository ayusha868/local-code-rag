import ollama

class RAGEngine:
    def __init__(self, indexer):
        self.indexer = indexer
        self.model_name = "qwen2.5-coder:1.5b"

    def generate_answer(self, user_query):
       
        relevant_chunks, metadatas = self.indexer.query_code(user_query, n_results=2)
        
        #  Formatting the context cleanly for the prompt
        context_str = ""
        for chunk, meta in zip(relevant_chunks, metadatas):
            context_str += f"\n--- File Context: {meta['source']} ---\n{chunk}\n"
            
        #  Constructing a zero-leak system prompt instruction set
        system_prompt = (
            "You are an expert code architect. Use the provided codebase snippets to answer the user's question accurately. "
            "If the answer cannot be found or inferred from the code context below, explicitly say that you don't know.\n\n"
            f"Codebase Context:\n{context_str}"
        )
        
        #  Prompting the local model instance
        response = ollama.chat(model=self.model_name, messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ])
        
        return response['message']['content'], metadatas