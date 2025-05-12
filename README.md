# AI Operations Copilot

A multi-functional AI assistant that can analyze documents, summarize content, plan tasks, and answer user queries.

## Tech Stack

- **Document Processing**: PyMuPDF, Pandas
- **Embedding & RAG**: OpenAI Embeddings, ChromaDB
- **Task Generation**: GPT-4, LangChain
- **Query Engine**: LangChain RetrievalQA
- **UI**: Streamlit
- **Voice Integration**: pyttsx3, SpeechRecognition

## Features

- 📄 Upload and analyze PDFs or Excel files
- 📊 Extract insights and summarize document content
- ✅ Generate task plans based on document content
- ❓ Answer questions about your documents
- 🎤 Optional voice commands

## Installation

To run this project locally, follow the steps below:

1. Clone this repository:
    ```bash
    git clone https://github.com/Harsha107/ai-operations-copilot

2. Install Python Virtual Environment (not necessary, but recommended):
    ```bash
    python -m venv your-environment-name

3. Run the environment:
    ```bash
    .\your-environment-name\Scripts\Activate

4. Install the packages from requirements.txt file:
    ```bash
    pip install -r requirements.txt

5. Create a `.env` file with your OpenAI AP key:
    ```bash
    OPENAI_API_KEY=your-api-key-here

6. Run the streamlit application:
    ```bash
    streamlit run app.py

7. After running the streamlit command, it should automatically open your device's default browser. If not, then open your browser and navigate to `http://localhost:8501`

## Usage

1. Upload a PDF or Excel file using the file uploader
2. Review the automatically generated summary
3. Check the suggested tasks and actions
4. Ask questions about your document in the "Ask Questions" tab
5. Toggle voice commands in the sidebar if needed