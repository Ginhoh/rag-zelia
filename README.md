# Projeto Zél-ia (RAG)


A Zélia é uma aplicação de Inteligência Artificial desenhada para atuar como assistente virtual universitária. Utiliza a arquitetura RAG (Retrieval-Augmented Generation) para processar o Manual do Aluno (e outros documentos) e responder de forma precisa a dúvidas académicas.

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
```

2. Crie e ative o ambiente virtual:
>Windows
```bash
.\.venv\Scripts\activate
```
>Mac e Linux
```bash
source .venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as varáveis de ambiente e insira a sua API Key do Google
```bash
GOOGLE_API_KEY=sua_chave_aqui_sem_aspas
```

### Execução do Projeto

Para correr a aplicação completa, necessitará de dois terminais abertos, ambos com o ambiente virtual (.venv) ativado.

**Terminal 1 (Backend - FastAPI):** Inicie a API executando o comando abaixo. O servidor ficará disponível em http://127.0.0.1:8000.
```bash
uvicorn main:app --reload
```

**Terminal 2 (Frontend - Streamlit):** Com o servidor a correr no primeiro terminal, inicie a interface gráfica no segundo. Um novo separador será aberto automaticamente no seu browser.
```bash
streamlit run app.py
```
