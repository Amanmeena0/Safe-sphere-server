from langchain_huggingface import HuggingFaceEndpointEmbeddings, ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

# Load and validate API Key
load_dotenv()
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not api_key:
    raise EnvironmentError("Missing HUGGINGFACEHUB_API_TOKEN in environment.")

# Load Chroma vector store
def load_vector_store():
    embeddings = HuggingFaceEndpointEmbeddings(
        huggingfacehub_api_token=api_key,
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
    # Use absolute path to ensure vector store is found
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persist_dir = os.path.join(current_dir, "chroma_langchain_db")
    db = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name="crime_qa_collection"
    )
    return db

# Build RAG chain
def build_rag_chain():
    vector_store = load_vector_store()
    
    # Add debug logging to check if the vector store has data
    try:
        collection = vector_store._collection
        count = collection.count()
        logging.info(f"✅ Vector store loaded with {count} documents")
    except Exception as e:
        logging.warning(f"Could not get document count: {e}")
    
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful assistant specialized in public safety and law.
Use the following context to answer the user's question.
If the context doesn't contain the answer, say "I don't have enough information on this topic."
Keep your answer concise and focused. STOP after providing the answer.

Context:
{context}

Question: {question}
Answer:"""
    )

    # Use meta-llama/Meta-Llama-3-8B-Instruct — confirmed to support HuggingFace's
    # chat completions router (router.huggingface.co/v1/chat/completions) which is
    # required by ChatHuggingFace. nvidia/Mistral-NeMo-12B-Instruct does NOT work here.
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        task="conversational",
        huggingfacehub_api_token=api_key,
        temperature=0.1,
        max_new_tokens=512,
    )
    model = ChatHuggingFace(llm=llm)



    rag_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )

    logging.info("✅ RAG chain initialized successfully.")
    return rag_chain

# Cache the chain globally
_rag_chain = None

def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        _rag_chain = build_rag_chain()
    return _rag_chain
