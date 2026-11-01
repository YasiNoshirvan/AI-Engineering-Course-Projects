# 🤖 AI Engineering Course Projects

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white) ![LangChain](https://img.shields.io/badge/Framework-LangChain-1C3C3C) ![LangGraph](https://img.shields.io/badge/Workflows-LangGraph-7952B3) ![Type](https://img.shields.io/badge/Type-Learning%20Repository-informational)

A collection of **10 hands-on Python exercises** completed while studying AI Engineering. The scripts move from basic LLM calls and text classification to **embeddings, RAG, agent tools, multi-agent coordination, and stateful LangGraph workflows**.

The goal is to document my learning process and keep practical experiments in one place. Some larger exercises are also presented as separate repositories.

## 📚 Topics covered

| Area | Examples |
| --- | --- |
| LLM applications | Chat completions, streaming, token usage, and conversation memory |
| NLP and embeddings | Zero-shot sentiment classification, sentence embeddings, and semantic similarity |
| Retrieval-Augmented Generation | PDF extraction, text chunking, ChromaDB, and document-based question answering |
| AI agents | Tool calling, live weather lookup, and supervisor-based multi-agent systems |
| Stateful workflows | LangGraph conditional edges, revision loops, and PostgreSQL checkpointing |
| Prompting and validation | Prompt templates, structured outputs, and Pydantic models |

## 📁 Repository contents

| File | What it explores |
| --- | --- |
| [`ChatBot.py`](ChatBot.py) | Streaming chatbot, session history, summarization, and token usage |
| [`SentimentAnalysis.py`](SentimentAnalysis.py) | Zero-shot sentiment classification with Transformers |
| [`embedding.py`](embedding.py) | Sentence embeddings and semantic similarity search |
| [`RAG.py`](RAG.py) | PDF-based question answering with embeddings and ChromaDB |
| [`Agent.py`](Agent.py) | Agent tool calling with live Open-Meteo weather data |
| [`Multi_agent.py`](Multi_agent.py) | Fruit-and-vegetable supervisor with specialist agents |
| [`Graph.py`](Graph.py) | Generate–review–revise loop with conditional graph edges |
| [`Checkpointer.py`](Checkpointer.py) | PostgreSQL-based conversation checkpoints and sessions |
| [`prompt_template.py`](prompt_template.py) | Prompt templates and Pydantic-validated structured outputs |
| [`pydantic_validation.py`](pydantic_validation.py) | Basic Pydantic field definitions and validation |

The repository also includes `symptoms.pdf` for the RAG exercise, as well as an earlier `Pipfile` / `Pipfile.lock` environment snapshot.

## ⚙️ Getting started

```bash
git clone https://github.com/YasiNoshirvan/AI-Engineering-Course-Projects.git
cd AI-Engineering-Course-Projects
```

Run individual exercises, for example:

```bash
python embedding.py
```

**Setup note:** These scripts were developed at different stages of the course and **do not all share one dependency set**. Some use an older Python 3.9 environment, while modern LangChain agent exercises require a newer environment (Python 3.12 was used). Install the libraries required by the specific script instead of assuming the older `Pipfile` covers everything.

Groq-based scripts require a local `.env` file with `GROQ_API_KEY`. The PostgreSQL exercise also needs `DATABASE_URL`, and the RAG exercise needs a compatible Chroma/SQLite setup. Never commit actual credentials or local database files.

## 🔎 Related standalone projects

Selected exercises were developed further as focused projects:

- 🍎 [FoodIQ — Multi-Agent Assistant](https://github.com/YasiNoshirvan/FoodIQ-Multi-Agent-Assistant)
- 🩺 [Medical Question Answering Using RAG](https://github.com/YasiNoshirvan/Medical-Question-Answering-Using-RAG)
- 💬 [Streaming LLM Chatbot](https://github.com/YasiNoshirvan/Streaming-LLM-ChatBot)

---

*Learning repository — practical experiments rather than production-ready AI applications.*
