https://github.com/user-attachments/assets/895fc846-ed16-40bc-bc44-2ceec099da3e

# 🧠 Website & PDF Summarizer App

A powerful and simple **Streamlit application** to summarize content from **websites** or **PDF documents**, and ask questions based on the summarized content using **Groq's LLaMA3-8B** model via **LangChain**.

---

## 🔧 Features

- 🌐 Summarize **Website URLs**
- 📄 Upload and summarize **PDF files**
- ❓ Ask **questions** based on the summarized content
- ⚡ Powered by **Groq LLaMA3-8B** (via LangChain)

---
# File Structure
```bash
├── app.py                   # Main Streamlit interface
├── summarizer.py            # Summarization and QA logic
├── requirements.txt         # List of required packages
└── .streamlit/
    └── secrets.toml         # Contains Groq API key
```
## How It Works

- For **websites**, content is extracted using `WebBaseLoader`.
- For **PDFs**, content is extracted using `UnstructuredPDFLoader`.
- Text is **truncated to 12,000 characters** to fit the model's input limit.
- **LangChain prompt templates** are used to generate:
  - 📄 A **concise summary**
  - ❓ **Context-based answers** to user questions


## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt

```
# Set Up Secrets
Create a file: .streamlit/secrets.toml and add your Groq API key:
```bash
groq_api_key = "your_groq_api_key_here"
```
# Run the App
```bash
streamlit run app.py
```


