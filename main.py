from core.parser import CodeParser
from core.indexer import LocalIndexer
from core.engine import RAGEngine

print(" Step 1: Parsing local source repositories...")
parser = CodeParser()
docs, metadatas = parser.parse_repository("./core")

print(" Step 2: Syncing updates to disk index...")
indexer = LocalIndexer()
indexer.index_code(docs, metadatas)

print(" Step 3: Spin up Local LLM Reasoning Context...")
engine = RAGEngine(indexer)

# Let's run a real test question asking the LLM to explain our own parser logic!
question = "Explain how the code parser ensures it doesn't break relative paths like ./core"
print(f"\n User Query: {question}")

answer, sources = engine.generate_answer(question)

print("\n AI Engineer Response:")
print(answer)