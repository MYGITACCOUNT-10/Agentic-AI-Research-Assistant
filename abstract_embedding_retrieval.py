#Prove that semantic retrieval works using abstracts only 
# After fetching a list of papers from the arXiv API, 
# this is exactly the code you use to find papers relevant to a topic using abstracts only.
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def build_vector_db(papers: list[dict]) -> Chroma:
    documents = [
        Document(
            page_content=p["abstract"],
            metadata={"title": p["title"], "arxiv_id": p["id"]}
        )
        for p in papers
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma.from_documents(documents, embeddings)


# for doc in results:
#     print("-----"*50)
#     print(f"Title: {doc.metadata['title']}")
#     print(f"Abstract: {doc.page_content}\n")
#     print("-----"*50)
#     print("\n")
