from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

# Load and validate API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("Missing GEMINI_API_KEY in environment.")
os.environ["GOOGLE_API_KEY"] = api_key  

# Load Chroma vector store
def load_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
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
You are a helpful assistant answering questions based on the following context:
If the context is not sufficient, you can answer based on your general knowledge.
IF the context about certain topics is not available, you would say "I don't have information on that topic."
and you should not make up information.
{context}

Question: {question}
Answer:
"""
    )

    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # ✅ Use valid available Gemini model
        temperature=0.2
    )

    rag_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )

    logging.info("✅ RAG chain initialized successfully.")
    return rag_chain
