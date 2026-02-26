import os
import logging
from dotenv import load_dotenv

# Importações do LangChain
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

# Configuração do logging para este arquivo também
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURAÇÃO E INICIALIZAÇÃO DOS COMPONENTES DE IA ---

# Carregamento robusto das variáveis de ambiente, igual ao process_data.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
load_dotenv(ENV_PATH)

PERSIST_DIRECTORY = os.path.join(SCRIPT_DIR, "chroma_db")

# VERIFICAÇÃO: Checar se o banco de dados existe antes de tentar carregar
if not os.path.exists(PERSIST_DIRECTORY):
    logging.error(f"Diretório do banco de dados não encontrado em '{PERSIST_DIRECTORY}'.")
    logging.error("Por favor, execute o script 'process_data.py' primeiro para criar o banco de dados.")
    # Em um cenário real, poderíamos usar sys.exit(1), mas aqui apenas avisamos.
    # A aplicação FastAPI ainda vai rodar, mas as buscas falharão.
    
# Inicializa o modelo de embeddings
logging.info("Inicializando o modelo de embeddings para consulta...")
embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# Carrega o banco de dados vetorial já existente
logging.info(f"Carregando o banco de dados vetorial de: {PERSIST_DIRECTORY}...")
vector_store = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embeddings_model
)

# Inicializa o modelo de linguagem (LLM)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
logging.info("Componentes de IA prontos.")

# (O resto da função get_rag_response continua exatamente o mesmo...)
def get_rag_response(query: str) -> str:
    logging.info(f"Iniciando busca por: '{query}'")
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    relevant_docs = retriever.invoke(query)

    context = ""
    for doc in relevant_docs:
        context += f"\nFonte: {doc.metadata.get('source', 'N/A')}, Página: {doc.metadata.get('page', 'N/A')}\n"
        context += f"Conteúdo: {doc.page_content}\n"
        context += "---\n"

    template = """
    Você é Zélia uma assistente prestativo do Centro Universitário Jorge Amado. Sua tarefa é responder à pergunta do aluno
    baseando-se SOMENTE no seguinte contexto extraído do Manual do Aluno e do Calendário Acadêmico.

    CONTEXTO:
    {context}

    PERGUNTA DO ALUNO:
    {question}

    INSTRUÇÕES:
    1. Responda de forma clara e direta.
    2. Se a resposta estiver no contexto, responda e CITE A FONTE E A PÁGINA de onde tirou a informação.
    3. Se a resposta NÃO ESTIVER no contexto, diga "Não encontrei essa informação nos documentos disponíveis. Por favor, procure a secretaria acadêmica."
    4. Não invente informações.
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    final_prompt = prompt.format(context=context, question=query)

    logging.info("Enviando prompt para o LLM...")
    response = llm.invoke(final_prompt)

    return response.content