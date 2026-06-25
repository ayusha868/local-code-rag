import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

class CodeParser:
    def __init__(self, supported_extensions=[".py", ".js", ".ts", ".java", ".cpp"]):
        self.supported_extensions = supported_extensions
        # This breaks code down logically by syntax rules (functions/classes) rather than raw character counts
        self.splitter = RecursiveCharacterTextSplitter.from_language(
            language="python", 
            chunk_size=800, 
            chunk_overlap=100
        )

    def parse_repository(self, repo_path):
        docs = []
        metadatas = []
        
        for root, _, files in os.walk(repo_path):
            # Check path segments to skip true hidden directories (like .git) or bulk package managers
            # We check len(part) > 1 to ensure standard relative dot paths (like './core') aren't skipped
            if any((part.startswith('.') and len(part) > 1) or part in ['node_modules', 'dist', 'venv', '__pycache__'] for part in root.split(os.sep)):
                continue
                
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in self.supported_extensions:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            code = f.read()
                        
                        # Break down this specific source file into code chunks
                        chunks = self.splitter.split_text(code)
                        
                        for i, chunk in enumerate(chunks):
                            docs.append(chunk)
                            # Enriching metadata makes your RAG system advanced and trackable
                            metadatas.append({
                                "source": os.path.relpath(file_path, repo_path),
                                "chunk_id": i
                            })
                    except Exception as e:
                        print(f"Skipping file due to read error {file_path}: {e}")
                        
        return docs, metadatas