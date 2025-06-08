from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


load_dotenv()

client = OpenAI()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="langchain_website_vectors",
    embedding=embedding_model,
)


def process_query(request):
    print("query in worker", request.query)

    search_similar_results = vector_db.similarity_search(query=request.query)

    context = ""

    for result in search_similar_results:
        content = result.page_content
        page = result.metadata.get("page_label", "N/A")
        source = result.metadata.get("source", "N/A")

        # print("content : ", content, "Page : ", page, "source : ", source)

        context += f"Page Content: {content}\nPage Number: {page}\nFile Location: {source}\n\n\n"

    SYSTEM_PROMPT = f"""
        You are a helpfull AI Assistant who asnweres user query based on the available context
        retrieved from a website along with page_contents and page source.

        You should only ans the user based on the following context and navigate the user
        to open the right page source to know more.

        Context:
        {context}
    """

    chat_completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.query},
        ],
    )


    print(f"🤖: {chat_completion.choices[0].message.content}")
