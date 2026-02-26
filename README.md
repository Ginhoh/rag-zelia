# Projeto Zél-ia (RAG)


A Zélia é uma aplicação "full-stack" de Inteligência Artificial desenhada para atuar como assistente virtual universitária. Utiliza a arquitetura RAG (Retrieval-Augmented Generation) para processar o Manual do Aluno e responder de forma precisa a dúvidas académicas.

## 🚀 Tecnologias Utilizadas

* **Modelo de IA:** Google Gemini (2.5 Flash para Chat, Gemini Embeddings para vetorização)
* **Orquestração de IA:** LangChain
* **Base de Dados Vetorial:** ChromaDB (Local)
* **Backend / API:** FastAPI + Uvicorn
* **Frontend:** Streamlit

## 🏗️ Arquitetura do Projeto

O projeto está dividido em três componentes principais:
1.  **Motor de Ingestão de Dados (`process_data.py`):** Lê ficheiros PDF, divide o texto em chunks, converte em embeddings e armazena no ChromaDB. Incorpora controlo de taxa de requisições (rate limiting) para APIs gratuitas.
2.  **Motor RAG e API (`rag_core.py` e `main.py`):** O backend que recebe perguntas via HTTP POST, realiza a busca semântica no ChromaDB e constrói o prompt de contexto para o modelo Gemini gerar a resposta final.
3.  **Interface de Utilizador (`app.py`):** Uma interface web interativa de chat desenvolvida em Streamlit, que comunica nativamente com o backend FastAPI.

## 🛠️ Como Executar Localmente

### Pré-requisitos
* Python 3.12+
* Chave de API do Google Gemini (Google AI Studio)

### Instalação

1. Clone o repositório:
```bash
git clone [https://github.com/Fau-Pereira/zelia.git](https://github.com/Fau-Pereira/zelia.git)
cd zelia