# Smart Document Agents 🧠📄

This project was built for the GenAI Hackathon 2025.

## 🚀 Problem Statement
Reading and analyzing long documents is time-consuming and error-prone.
We solve this with AI agents that:
- Summarize the document
- Extract entities and sentiment

## 🔁 Workflow
1. User uploads a `.txt` file
2. Summarizer Agent generates a short summary
3. Insight Agent extracts named entities and sentiment
4. All results are shown in an easy-to-use Streamlit interface

## 🛠️ Tech Stack
- Streamlit (Frontend)
- HuggingFace Transformers
- spaCy
- TextBlob
- GenAI AgentOS Protocol

## 🎥 Demo Video
_Link to be added_

## 📁 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
