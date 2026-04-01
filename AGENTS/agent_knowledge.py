import json
from typing import Annotated

from langchain_core.documents import Document

from Lib.log import logger
from PLUGINS.Embeddings.embeddings_qdrant import embedding_api_singleton_qdrant, SIRP_KNOWLEDGE_COLLECTION


class AgentKnowledge(object):

    @staticmethod
    def internal_knowledge_base_search(
            query: Annotated[
                str, "The search query, can be an entity (IP, Email, Domain) or a business concept/rule description or "
                     "anything you want to know from internal knowledge base."]
    ) -> Annotated[str, "A List of string containing relevant knowledge entries, policies, and special handling instructions."]:
        """
        Search the internal knowledge base for specific entities, business-specific logic, SOPs, or historical context.
        """
        logger.debug(f"knowledge search : {query}")
        threshold = 0.8
        result_all = []
        docs_qdrant = embedding_api_singleton_qdrant.search_documents_with_rerank(collection_name=SIRP_KNOWLEDGE_COLLECTION, query=query, k=10, top_n=3)
        logger.debug(docs_qdrant)
        for doc in docs_qdrant:
            doc: Document
            if doc.metadata["rerank_score"] >= threshold:
                result_all.append(doc.page_content)

        results = json.dumps(result_all, ensure_ascii=False)
        logger.debug(f"Knowledge search results : {results}")
        return results
