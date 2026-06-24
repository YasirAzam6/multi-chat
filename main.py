from core.tenant_manager import tenant_manager
# from ingestion.loaders.generic_loader import GenericLoader
# from ingestion.cleaners.text_cleaner import TextCleaner
# from ingestion.chunking.recursive_chunker import RecursiveChunker
# from embeddings.embedding_router import EmbeddingRouter
from core.logging_config import setup_logging
# from vectorstores.supabase_store import supa_base_vector_db
# from retrieval.retrieval_router import RetrievalRouter
# from retrieval.rerankers.reraker_openai import RerankerOpenAI
# from llm.prompt_manager import PromptManager
# from llm.llm_router import LLMRouter
from graph.rag_graph import build_graph
from core.server import app 
import uvicorn
import sys
# tenant = tenant_manager.load_tenant(tenant_id="tenant_1")
# print("Loaded Tenant: ", tenant.tenant_id)
# print("Tenant Configuration:", tenant.config)
# print("Prompts Path:", tenant.prompts_path)
# print("Docs Path:", tenant.docs_path)
# print("Bits Path:", tenant.bits_path)
# print("Tenant loaded successfully.")

# ****************************************************

setup_logging()

def run_cli():

    tenant = tenant_manager.load_tenant(tenant_id="tenant_1")
    # print("Loaded Tenant: ", tenant.tenant_id)
    # print("Tenant Configuration:", tenant.config)
    # print("Prompts Path:", tenant.prompts_path)
    # print("Docs Path:", tenant.docs_path)
    # print("Bits Path:", tenant.bits_path)
    # print("Tenant loaded successfully.")
    print("Tenant Configuration:", tenant.config)
    print("System Prompt:", tenant.config.get("system_prompt"))
    print("Style Prompt:", tenant.config.get("style_prompt"))


    my_graph = build_graph()
    print("RAG Graph built successfully.")
    # mermaid_code = my_graph.get_graph().draw_mermaid()
    # print(mermaid_code)
    while True:
        input_query = input("Enter your query (or 'exit' to quit): ")
        if input_query.lower() == 'exit':
            break
        else:
            state = {
                "query": input_query,
                "tenant_id" : "tenant_1"
            }
            config_var = {"configurable": {
                "thread_id" : "thread_11",
            }}

            result = my_graph.invoke(state, config=config_var)
            print("Answer:", result['answer'])

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000
        )

# ****************************************************



# router = RetrievalRouter(tenant)
# retrieval = router.get_retriever()
# question = "What is the project overview?"
# retrieved_docs = retrieval.retrieve(question)
# for doc in retrieved_docs:
    # print("*"*50)
    # print(doc.page_content)
    # print("*"*50)
# re_ranker = RerankerOpenAI()
# re_ranked_docs = re_ranker.rerank(question, retrieved_docs)
# print("Re-ranked Documents:")
# for doc in re_ranked_docs:
#     print("*"*50)
#     print(doc.page_content)
#     print("*"*50)

# prompt_manager = PromptManager(tenant=tenant)
# final_prompt = prompt_manager.build_full_prompt(user_query=question, context_docs=re_ranked_docs)
# llm = LLMRouter(tenant=tenant).get_llm()

# answer = llm.generate(final_prompt)

# print("*"*50)
# print("Answer is :", answer)
# print("*"*50)

# # Document Loading Section
# loader = GenericLoader()
# docs = loader.load(tenant.docs_path + "/Sharaka AI Portal.pdf")
# print(f"Loaded {len(docs)} documents.")

# # Cleaning Section
# cleaner = TextCleaner()
# clean_docs = cleaner.clean(docs)
# print("Documents cleaned.")




