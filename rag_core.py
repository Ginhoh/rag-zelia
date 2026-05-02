import os
from datetime import datetime
from dotenv import load_dotenv

# Importações atualizadas
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
#from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool
from langchain.agents import create_agent

import asyncio
from get_webdata import main

load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIRECTORY = os.path.join(SCRIPT_DIR, "chroma_db")

# 1. Configurar Modelos
embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# 2. Conectar ao Banco de Dados Vetorial
vector_store = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embeddings_model
)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})


# ==========================================
# 🛠️ CRIAÇÃO DAS FERRAMENTAS DO AGENTE
# ==========================================

@tool
def pesquisa_base_conhecimento(query: str) -> str:
    """Pesquisa informações oficiais nos documentos da universidade. Use SEMPRE esta ferramenta para responder a dúvidas institucionais ou regras."""
    docs = retriever.invoke(query)
    
    contextos_formatados = []
    for doc in docs:
        fonte = os.path.basename(doc.metadata.get('source', 'Documento Desconhecido'))
        pagina = doc.metadata.get('page', 'N/A')
        bloco = f"[ARQUIVO: {fonte} | PÁGINA: {pagina}]\n{doc.page_content}"
        contextos_formatados.append(bloco)
        
    return "\n\n---\n\n".join(contextos_formatados)

@tool
def consultar_data_atual() -> str:
    """Consulta a data e hora atual do sistema em tempo real. Use esta ferramenta para saber o dia de hoje ao calcular prazos."""
    agora = datetime.now()
    return agora.strftime("%d/%m/%Y, %H:%M")

@tool
def consultar_eventos() -> str:
    """Consulta os dados informando sobre os eventos institucionais. De primeira vista, os dados estarão como se acabassem de ser colados, você organizará os dados de acordo com cada evento, e retornará com precisão de acordo com o que o usuário pedir. Use sempre que o usuário pedir informação sobre algum evento."""
    return asyncio.run(main())

ferramentas = [pesquisa_base_conhecimento, consultar_data_atual, consultar_eventos]


# ==========================================
# 🧠 CONFIGURAÇÃO DO AGENTE LANGGRAPH
# ==========================================

INSTRUCOES_SISTEMA = """Você é a Zélia, uma assistente virtual autónoma da universidade.
Você tem ferramentas ao seu dispor. Sempre que não souber algo, pare e use a ferramenta apropriada.
Se usar a 'pesquisa_base_conhecimento', lembre-se OBRIGATORIAMENTE de citar a fonte da informação no final da sua resposta (ex: Fonte: calendario.pdf, Página 2).
Seja amigável, clara e direta."""

# Cria o agente autónomo BÁSICO (Sem modificadores que causam erro de versão)
agente = create_agent(llm, ferramentas)


# ==========================================
# 🚀 FUNÇÃO DE COMUNICAÇÃO (Chamada pela API)
# ==========================================
def get_rag_response(query: str, history: list = None) -> str:
    if history is None:
        history = []
        
    # Colocamos a instrução do sistema diretamente como a PRIMEIRA mensagem
    mensagens = [
        ("system", INSTRUCOES_SISTEMA)
    ]
    
    # 1. Injeta o histórico da conversa
    for msg in history[-4:]: 
        if msg["role"] == "user":
            mensagens.append(("human", msg["content"]))
        else:
            mensagens.append(("ai", msg["content"]))
            
    # 2. Injeta a pergunta nova do aluno
    mensagens.append(("human", query))

   # 3. O Agente entra em ação, escolhe as ferramentas e responde
    resposta = agente.invoke({"messages": mensagens})
    
    conteudo_bruto = resposta["messages"][-1].content
    
    # Se a resposta vier como um "pacote de dados" (lista com assinatura), extraímos só o texto
    if isinstance(conteudo_bruto, list):
        for bloco in conteudo_bruto:
            if isinstance(bloco, dict) and 'text' in bloco:
                return bloco['text']
        return str(conteudo_bruto) # Fallback de segurança
        
    # Se já vier como texto simples, devolvemos direto
    return conteudo_bruto

