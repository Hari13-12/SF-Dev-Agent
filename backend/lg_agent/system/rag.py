from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from lg_agent.core.state_model import State

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

faiss_index = FAISS.load_local(
    r"D:\Shi-SF-Agent\sample_agent\my_faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = faiss_index.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
    

def edit_object_rag(state: State):
    print("RAG invoked")
    query = state["messages"][-1].content
    try:
        results = retriever.get_relevant_documents(query)
        print("Used retriever.get_relevant_documents")
    except AttributeError:
        query_emb = embeddings.embed_query(query)
        docs_and_scores = faiss_index.similarity_search_with_score_by_vector(query_emb, k=3)
        results = [doc.page_content for doc, _ in docs_and_scores]
        lines = results[0].splitlines()
        object_name = lines[0].replace("Object:", "").strip()
        # fields = [line.replace("- ", "") for line in lines if line.startswith("- ")]
        state["obj_name"] = object_name
        return state
    except Exception as e:
        print("Exception occurred during RAG process", str(e))
        state["response"] = f"Exception occurred during RAG process : {str(e)}"
        return state


# print(return_relevant_documents("alter the custom object object of meter reading"))