from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document

class TaskPlanner:
    """Generates a task and actions based on document content."""

    def __init__(self, api_key: str = None):
        """Initialize the task planner."""

        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4",
            api_key=api_key
        )

        self.task_prompt = ChatPromptTemplate.from_template(
            """You are an AI operations assistant that helps users plan tasks based on document content.
            
            Based on the following document content, identify key tasks, actions, or follow-ups that should be taken.
            If there are deadlines, priorities, or responsible parties mentioned, include those in your plan.
            
            Document content:
            {document_content}
            
            Generate a structured task plan with:
            1. Summary of the situation
            2. List of specific tasks/actions (with deadlines if applicable)
            3. Prioritization of tasks (High/Medium/Low)
            4. Any dependencies between tasks
            
            Present your response in a clear, structured format.
            """
        )

        self.task_chain = LLMChain(
            llm=self.llm,
            prompt=self.task_prompt
        )

    def generate_tasks(self, relevant_docs: List[Document]) -> str:
        """Generate tasks based on relevant document chunks."""

        # Combine the content from all relevant documents
        combined_content = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Generate tasks
        result = self.task_chain.run(document_content=combined_content)

        return result
    
    def generate_summary(self, full_content: str) -> str:
        """Generate a summary of the entire document."""

        summary_prompt = ChatPromptTemplate.from_template(
            """You are an AI operations assistant that helps users understand documents.
            
            Please provide a comprehensive summary of the following document content.
            Highlight key points, important figures, dates, and actionable insights.

            Document content:
            {document_content}

            Your summary should be concise but thorough, covering all important aspects of the document.
            """
        )

        summary_chain = LLMChain(
            llm=self.llm,
            prompt=summary_prompt,
        )

        return summary_chain.run(document_content=full_content)