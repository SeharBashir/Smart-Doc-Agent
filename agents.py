
from transformers import pipeline
import spacy
from textblob import TextBlob

# Load summarizer and NLP model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
nlp = spacy.load("en_core_web_sm")

def split_text(text, max_tokens=1000):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield " ".join(words[i:i + max_tokens])

def run_summarizer(text):
    summaries = []
    for chunk in split_text(text, max_tokens=500):  # smaller chunks
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return "\n\n".join(summaries)

def run_insight_agent(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    sentiment = TextBlob(text).sentiment
    return entities, sentiment
