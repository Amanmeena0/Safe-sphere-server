from langchain_community.document_loaders import RecursiveUrlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import time
import logging
from random import uniform


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("Missing GEMINI_API_KEY in environment.")
os.environ["GOOGLE_API_KEY"] = api_key

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recursive_scrape(url, max_depth=3, delay=1):
    """
    Recursively scrape a URL and its linked pages up to a specified depth.
    Introduces a delay to avoid overwhelming the server.
    """
    if max_depth < 0:
        return ""

    logger.info(f"🔍 Scraping {url} at depth {max_depth}...")
    time.sleep(uniform(0.5, delay))  # Random delay between 0.5 and delay seconds

    try:
        loader = RecursiveUrlLoader(url, max_depth=max_depth)
        documents = loader.load()
        text_content = "\n".join(doc.page_content for doc in documents)
        logger.info(f"✅ Successfully scraped {len(documents)} documents from {url}.")
        return text_content
    except Exception as e:
        logger.error(f"❌ Error scraping {url}: {e}")
        return ""

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return splitter.split_text(text)


def create_vector_store(chunks):
    if not chunks:
        raise ValueError("No text chunks to embed.")

    logger.info(f"🔍 Total chunks to embed: {len(chunks)}")
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    try:
        test_emb = embeddings_model.embed_query("test")
        logger.info(f"✅ Gemini Embeddings working. Sample output length: {len(test_emb)}")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to connect to Gemini Embeddings API: {e}")

    filtered_chunks = [chunk for chunk in chunks if chunk.strip()]
    if not filtered_chunks:
        raise ValueError("❌ All chunks are empty or whitespace.")

    logger.info("🚀 Creating vector store with filtered chunks...")
    # Use absolute path to ensure consistency
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persist_dir = os.path.join(current_dir, "chroma_langchain_db")
    vector_store = Chroma.from_texts(
        texts=filtered_chunks,
        embedding=embeddings_model,
        collection_name="crime_qa_collection",
        persist_directory=persist_dir
    )
    vector_store.persist()
    logger.info("✅ Vector store persisted successfully.")
    return vector_store


if __name__ == "__main__":
    # Combine questions and answers for better context
    questions_file = "./crime_questions.txt"
    answers_file = "./crime_answers.txt"
    
    try:
        with open(questions_file, "r", encoding="utf-8") as f:
            questions = f.readlines()
        with open(answers_file, "r", encoding="utf-8") as f:
            answers = f.readlines()
        
        # Combine questions and answers
        combined_texts = []
        for q, a in zip(questions, answers):
            q = q.strip()
            a = a.strip()
            if q and a:
                # Create Q&A pairs for better retrieval
                combined_text = f"Question: {q}\nAnswer: {a}"
                combined_texts.append(combined_text)
        
        logger.info(f"✅ Created {len(combined_texts)} Q&A pairs")
        
        if combined_texts:
            chunks = chunk_text("\n\n".join(combined_texts))
            create_vector_store(chunks)
            logger.info("✅ Vector store creation from Q&A pairs completed.")
        else:
            logger.error("❌ No Q&A pairs created")
            
    except Exception as e:
        logger.error(f"❌ Error processing files: {e}")
