import streamlit as st
import os
import pandas as pd
import tempfile
import io
from dotenv import load_dotenv
from utils.document_processor import DocumentProcessor
from utils.embedding_engine import EmbeddingEngine
from utils.task_planner import TaskPlanner
from utils.query_engine import QueryEngine
from utils.voice_handler import VoiceHandler

load_dotenv()

st.set_page_config(
    page_title="AI Operations Copilot",
    page_icon="🤖",
    layout="wide"
)

if "processed_file" not in st.session_state:
    st.session_state.processed_file = False
if "full_text" not in st.session_state:
    st.session_state.full_text = ""
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "tasks" not in st.session_state:
    st.session_state.tasks = ""
if "embedding_engine" not in st.session_state:
    st.session_state.embedding_engine = None
if "query_engine" not in st.session_state:
    st.session_state.query_engine = None
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False
if "excel_data" not in st.session_state:
    st.session_state.excel_data = {}

@st.cache_resource
def initialize_components():
    api_key = os.getenv("OPENAI_API_KEY")
    document_processor = DocumentProcessor()
    embedding_engine = EmbeddingEngine(api_key=api_key)
    task_planner = TaskPlanner(api_key=api_key)
    voice_handler = VoiceHandler()
    
    return document_processor, embedding_engine, task_planner, voice_handler

document_processor, embedding_engine, task_planner, voice_handler = initialize_components()

st.title("🤖 AI Operations Copilot")
st.markdown("""
Upload a PDF or Excel file to analyze, extract insights, and plan tasks.
Ask questions about your documents and get instant answers!
""")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.session_state.voice_enabled = st.toggle("Enable Voice Commands", value=False)
    
    if st.session_state.voice_enabled:
        if st.button("🎤 Speak a question"):
            user_question = voice_handler.speech_to_text()
            if user_question:
                st.session_state.user_question = user_question

uploaded_file = st.file_uploader("Upload a document (PDF or Excel)", type=["pdf", "xlsx", "xls"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]
    
    with st.spinner(f"Processing {file_type.upper()} file..."):
        file_content = uploaded_file.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        
        st.session_state.full_text, st.session_state.chunks = document_processor.process_file(file_content, file_type)
        
        if file_type.lower() in ["xlsx", "xls"]:
            try:
                excel_file = pd.ExcelFile(io.BytesIO(file_content))
                st.session_state.excel_data = {
                    sheet_name: pd.read_excel(io.BytesIO(file_content), sheet_name=sheet_name)
                    for sheet_name in excel_file.sheet_names
                }
            except Exception as e:
                st.error(f"Error processing Excel data: {e}")
        
        st.session_state.embedding_engine = embedding_engine
        vector_store = embedding_engine.create_embeddings(st.session_state.chunks)
        
        st.session_state.query_engine = QueryEngine(vector_store, api_key=api_key)
        
        st.session_state.summary = task_planner.generate_summary(st.session_state.full_text)
        
        relevant_docs = embedding_engine.retrieve_relevant_chunks("important tasks deadlines priorities", k=5)
        st.session_state.tasks = task_planner.generate_tasks(relevant_docs)
        
        st.session_state.processed_file = True
        
        os.unlink(tmp_path)

if st.session_state.processed_file:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Summary", "✅ Tasks & Actions", "❓ Ask Questions", "📊 Data Preview", "🔍 Raw Content"])
    
    with tab1:
        st.header("Document Summary")
        st.markdown(st.session_state.summary)
    
    with tab2:
        st.header("Recommended Tasks & Actions")
        st.markdown(st.session_state.tasks)
    
    with tab3:
        st.header("Ask Questions About Your Document")
        
        if st.session_state.voice_enabled:
            if "user_question" in st.session_state:
                user_question = st.text_input("Your question:", value=st.session_state.user_question)
                st.session_state.user_question = ""
            else:
                user_question = st.text_input("Your question:")
        else:
            user_question = st.text_input("Your question:")
        
        if user_question:
            with st.spinner("Thinking..."):
                answer = st.session_state.query_engine.query(user_question)
                st.markdown("### Answer")
                st.markdown(answer)
                
                if st.session_state.voice_enabled:
                    voice_handler.text_to_speech(answer)
    
    with tab4:
        st.header("Data Preview")
        
        if hasattr(st.session_state, 'excel_data') and st.session_state.excel_data:
            for sheet_name, df in st.session_state.excel_data.items():
                with st.expander(f"Sheet: {sheet_name}"):
                    st.dataframe(df, use_container_width=True)
                    
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        st.subheader("Numeric Data Statistics")
                        st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label=f"Download {sheet_name} as CSV",
                        data=csv,
                        file_name=f"{sheet_name}.csv",
                        mime="text/csv"
                    )
        else:
            st.info("Data preview is available for Excel files. For PDFs, please see the Raw Content tab.")
    
    with tab5:
        st.header("Raw Document Content")
        st.text(st.session_state.full_text[:5000] + ("..." if len(st.session_state.full_text) > 5000 else ""))
        
        if st.checkbox("Show document chunks"):
            for i, chunk in enumerate(st.session_state.chunks):
                with st.expander(f"Chunk {i+1} - {chunk['metadata'].get('source', 'Unknown')}"):
                    st.write(chunk["metadata"])
                    st.text(chunk["content"][:500] + ("..." if len(chunk["content"]) > 500 else ""))

st.markdown("---")
st.markdown("AI Operations Copilot - Turning documents into decisions")