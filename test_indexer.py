from core.parser import CodeParser
from core.indexer import LocalIndexer

# 1. Parse the core folder
parser = CodeParser()
docs, metadatas = parser.parse_repository("./core")

# 2. Feed parsed files into our new local indexer
indexer = LocalIndexer()
indexer.index_code(docs, metadatas)

# 3. Test a natural language question (semantic query!)
print("\n🔍 Testing Semantic Vector Search...")
matched_docs, matched_metadatas = indexer.query_code("Where do we skip hidden directories?")

if matched_docs:
    print(f"\n✨ Closest Match Found in: {matched_metadatas[0]['source']}")
    print("--- Matched Snippet ---")
    print(matched_docs[0])