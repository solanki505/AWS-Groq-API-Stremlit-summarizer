import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.pdf import UnstructuredPDFLoader
from tempfile import NamedTemporaryFile

try:
    api_key = st.secrets["groq_api_key"]
    os.environ["USER_AGENT"] = "summarizer/1.0"

    model = ChatGroq(
        model_name="llama3-8b-8192",
        groq_api_key=api_key
    )

    summary_prompt = PromptTemplate.from_template(
        '''
        Analyze and summarize the following content in 50 to 100 words:
        
        {page_data}
        '''
    )
    summary_chain = summary_prompt | model


    qa_prompt = PromptTemplate.from_template(
        '''
        Given the following context:

        {context}

        Answer the following question based only on the provided context:
        {question}
        '''
    )
    qa_chain = qa_prompt | model

except Exception as e:
    st.error(f"Error initializing language model: {e}")
    summary_chain = None
    qa_chain = None


MAX_INPUT_CHARS = 12000

def answer_question(question: str, context: str) -> str:
    """
    Answers a question based on the provided context.

    Args:
        question: The user's question.
        context: The text content from the summarized document.

    Returns:
        The answer to the question.
    """
    if not qa_chain:
        return "Error: The question-answering model is not available."
    if not context:
        return "No context available. Please summarize a document first."
    if not question:
        return "Please enter a question."
        
    try:
        response = qa_chain.invoke({
            "context": context,
            "question": question
        })
        return response.content
    except Exception as e:
        return f"An error occurred while getting the answer: {e}"


def summarize_website(url: str) -> tuple[str, str]:
    """
    Summarizes a website and returns the summary and the full content.

    Args:
        url: The URL of the website to summarize.

    Returns:
        A tuple containing the summary (str) and the full page content (str).
    """
    if not summary_chain:
        return "Error: The summarization model is not available.", ""
    try:
        loader = WebBaseLoader(url)
        page = loader.load()
        if not page:
            return "Error: No content found on the page.", ""
            
        content = page[0].page_content[:MAX_INPUT_CHARS]
        
        res = summary_chain.invoke({'page_data': content})
        summary = res.content if hasattr(res, "content") else str(res)
        return summary, content
        
    except Exception as e:
        return f"Error processing website: {e}", ""


def summarize_pdf(uploaded_file) -> tuple[str, str]:
    """
    Summarizes a PDF and returns the summary and the full content.

    Args:
        uploaded_file: The uploaded PDF file object from Streamlit.

    Returns:
        A tuple containing the summary (str) and the full PDF text content (str).
    """
    if not summary_chain:
        return "Error: The summarization model is not available.", ""
    try:
        # Save PDF temporarily to read it
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        loader = UnstructuredPDFLoader(temp_file_path)
        docs = loader.load()
        
        all_text = " ".join([doc.page_content for doc in docs])
        all_text_truncated = all_text[:MAX_INPUT_CHARS]
        
        res = summary_chain.invoke({'page_data': all_text_truncated})
        summary = res.content if hasattr(res, "content") else str(res)

        os.remove(temp_file_path)  # Clean up the temporary file
        
        # Return the summary and the full text (not truncated) for context
        return summary, all_text

    except Exception as e:
        return f"Error processing PDF: {e}", ""
