import streamlit as st
from summarizer import summarize_website, summarize_pdf, answer_question

st.title("🧠 Website or PDF Summarizer")

if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'context' not in st.session_state:
    st.session_state.context = ""
if 'answer' not in st.session_state:
    st.session_state.answer = ""

option = st.radio("Choose input type:", ("Website URL", "Upload PDF"), key="input_option")

if option == "Website URL":
    url = st.text_input("Enter website URL", "https://www.example.com/")
    if st.button("Summarize Website"):
        with st.spinner("Summarizing website..."):
            # The summarize functions now return both summary and context
            summary, context = summarize_website(url)
            # We store both in our session state
            st.session_state.summary = summary
            st.session_state.context = context
            st.session_state.answer = "" # Clear previous answer

elif option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file and st.button("Summarize PDF"):
        with st.spinner("Summarizing PDF..."):
            # The summarize functions now return both summary and context
            summary, context = summarize_pdf(uploaded_file)
            # We store both in our session state
            st.session_state.summary = summary
            st.session_state.context = context
            st.session_state.answer = "" # Clear previous answer

# --- Display Summary ---
# We check if a summary exists in our session state and display it.
if st.session_state.summary:
    st.subheader("Summary:")
    st.write(st.session_state.summary)

    # --- Question Answering Section ---
    # This section will only appear after a summary has been generated.
    st.subheader("Ask a Question")
    user_question = st.text_input("Your question based on the content above:")
    
    if st.button("Get Answer"):
        if user_question:
            with st.spinner("Thinking..."):
                # We pass the user's question AND the stored context to the function.
                answer = answer_question(user_question, st.session_state.context)
                st.session_state.answer = answer
        else:
            st.warning("Please enter a question.")

# --- Display Answer ---
if st.session_state.answer:
    st.markdown("**Answer:**")
    st.write(st.session_state.answer)
