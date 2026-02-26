from fastapi import FastAPI
from pydantic import BaseModel

# Importa a função principal do nosso outro arquivo
from rag_core import get_rag_response

# Cria a instância da aplicação FastAPI
app = FastAPI()

# Define o modelo de dados para a pergunta que chegará via API
class Question(BaseModel):
    query: str


# --- ENDPOINT DA API ---

@app.post("/perguntar")
async def perguntar_ao_manual(question: Question):
    """
    Endpoint da API que recebe uma pergunta, chama a lógica do RAG,
    e retorna a resposta.
    """
    print(f"API recebeu a pergunta: {question.query}")
    # Chama a função do rag_core.py para fazer todo o trabalho pesado
    answer = get_rag_response(question.query)
    return {"answer": answer}