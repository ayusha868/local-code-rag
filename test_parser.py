from core.parser import CodeParser

# Initialize parser
parser = CodeParser()

# Point this to your current core folder to test it on itself!
target_folder = "./core" 

docs, metadatas = parser.parse_repository(target_folder)

print(f"🎉 Successfully parsed {len(docs)} structural code chunks!")
if docs:
    print("\n--- Sample Metadata ---")
    print(metadatas[0])
    print("\n--- Sample Code Chunk ---")
    print(docs[0])