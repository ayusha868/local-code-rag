import streamlit as st
from core.parser import CodeParser
from core.indexer import LocalIndexer
from core.engine import RAGEngine

# Page configuration
st.set_page_config(page_title="Local Code RAG Engine", layout="wide", page_icon="💻")

@st.cache_resource
def init_rag_system():
    # Cache components so they don't reload on every button click
    indexer = LocalIndexer()
    parser = CodeParser()
    engine = RAGEngine(indexer)
    return parser, indexer, engine

parser, indexer, engine = init_rag_system()

st.title("High-Throughput Local Code RAG Engine")
st.write("Analyze and query your codebase completely offline with zero data leaks.")
st.write("---")

# Layout: Sidebar for controls, Main area for chat
with st.sidebar:
    st.header(" Codebase Indexer")
    repo_path = st.text_input("Target Folder Path:", value="./core")
    
    if st.button("Build / Update Index", use_container_width=True):
        with st.spinner("Scanning and vectorizing repository..."):
            docs, metadatas = parser.parse_repository(repo_path)
            indexer.index_code(docs, metadatas)
            st.success(f"Successfully indexed {len(docs)} code chunks!")

# Main Conversation Stream
user_query = st.text_input(" Ask a structural or architectural question:", placeholder="e.g., How do we skip hidden directories?")

if user_query:
    with st.spinner("LLM Reasoning in progress..."):
        answer, sources = engine.generate_answer(user_query)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("###  AI Architect Response")
            st.write(answer)
            
        with col2:
            st.markdown("###  Referenced Code Context")
            # De-duplicate sources
            unique_sources = set([s['source'] for s in sources])
            for src in unique_sources:
                st.info(f" `{src}`")