# 📄 Smart Document Agents

An intelligent Streamlit app that uses AI agents to analyze documents (TXT, PDF, DOCX, DOC). Built for the GenAI AgentOS Protocol Hackathon.

## 🚀 Features

- Upload TXT, PDF, DOC, or DOCX documents
- Summarizes using HuggingFace BART
- Named entity extraction with spaCy
- Sentiment analysis with TextBlob
- Stylish, user-friendly interface
- Uses **2 AI agents** independently

## 🧠 Agents Used

| Agent          | Description                            |
|----------------|----------------------------------------|
| 🧾 Summarizer   | Extracts concise summary using transformers |
| 🔍 Insight Agent| Extracts named entities & sentiment using spaCy + TextBlob |

## 📽 Demo

Watch this short video: [Demo Video Link]

## 🛠 How to Run

```bash
git clone https://github.com/sehar/smart_doc_agents.git
cd smart_doc_agents
python -m venv venv
venv\Scripts\activate  # for Windows
pip install -r requirements.txt
streamlit run app.py
