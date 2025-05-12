from typing import List, Dict, Any
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.vectorstores import VectorStore
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

class QueryEngine:
    """Handles user queries about document content."""

    def __init__(self, vector_store: VectorStore, api_key: str = None):
        """Initialize the query engine."""

        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4",
            api_key=api_key
        )

        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(),
            return_source_documents=True
        )

        # Creating tools for the agent
        tools = [
            Tool(
                name="Document QA",
                func=self.qa.run,
                description="Useful for answering questions about the document content."
            )
        ]

        # Initializing the agent
        self.agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def query(self, question: str) -> str:
        """Answer a question based on the document content."""

        try:
            return self.agent.run(question)
        except Exception as e:
            return self.qa.run(question)