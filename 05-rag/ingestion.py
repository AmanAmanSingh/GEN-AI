from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


load_dotenv()
client = OpenAI()

# Load the webpage
loader = WebBaseLoader("https://python.langchain.com/docs/integrations/document_loaders/")
docs = loader.load()

# Clean the content to remove unwanted \n, extra spaces, headers/footers
def clean_text(text: str) -> str:
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 30]  # remove short/noisy lines
    return '\n\n'.join(cleaned_lines)

# Clean the page_content before creating Document
cleaned_content = clean_text(docs[0].page_content)

doc = Document(
    page_content=cleaned_content,
    metadata=docs[0].metadata
)

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=200
)

split_docs = text_splitter.split_documents(documents=[doc])  # use cleaned `doc`

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="langchain_website_vectors",
    embedding=embedding_model
)

print("splitted docs:", split_docs)
