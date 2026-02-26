import os
import sys
import logging
import time # NOVO: Importamos a biblioteca de tempo para as pausas
from dotenv import load_dotenv

# Importações do LangChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
load_dotenv(ENV_PATH) 

DEFAULT_PDF_FILE_PATH = os.path.join(SCRIPT_DIR, "uj_manual_do_aluno.pdf") 
DEFAULT_PERSIST_DIRECTORY = os.path.join(SCRIPT_DIR, "chroma_db")

def processar_e_salvar_documentos(pdf_path: str, persist_directory: str):
    logging.info("--- Início do Processamento ---")

    if not os.getenv("GOOGLE_API_KEY"):
        logging.error("A variável de ambiente GOOGLE_API_KEY não foi encontrada.")
        sys.exit(1) 
    
    # 1. CARREGAR O DOCUMENTO PDF
    logging.info(f"Carregando o documento: {pdf_path}...")
    try:
        loader = PyPDFLoader(pdf_path)
        documentos = loader.load()
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado em: {pdf_path}")
        return
    
    if not documentos:
        logging.warning("Nenhum documento foi carregado. Verifique o conteúdo do arquivo.")
        return
    logging.info(f"Documento carregado com sucesso. {len(documentos)} páginas encontradas.")

    # 2. DIVIDIR O DOCUMENTO EM PEDAÇOS (CHUNKS)
    logging.info("Dividindo o texto em pedaços (chunks)...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_divididos = text_splitter.split_documents(documentos)
    logging.info(f"O documento foi dividido em {len(docs_divididos)} chunks.")

    # 3. CRIAR O MODELO DE EMBEDDINGS (Modelo Correto!)
    logging.info("Inicializando o modelo de embeddings do Google...")
    embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    # 4. CRIAR E SALVAR O BANCO DE DADOS VETORIAL COM PAUSAS (Lógica Nova)
    logging.info(f"Criando banco de dados vetorial em: {persist_directory}...")
    
    # Inicializa o Chroma vazio
    vector_store = Chroma(
        embedding_function=embeddings_model,
        persist_directory=persist_directory
    )

    # Define o tamanho do lote (batch) que o Google aguenta sem estourar o limite. 
    # Vamos enviar de 20 em 20 pedaços.
    tamanho_lote = 20
    
    for i in range(0, len(docs_divididos), tamanho_lote):
        lote = docs_divididos[i : i + tamanho_lote]
        logging.info(f"Processando lote de chunks {i+1} até {min(i + tamanho_lote, len(docs_divididos))} de {len(docs_divididos)}...")
        
        # Adiciona o lote ao banco de dados
        vector_store.add_documents(lote)
        
        # Se não for o último lote, faz uma pausa de 10 segundos para não estourar a API
        if (i + tamanho_lote) < len(docs_divididos):
            logging.info("Pausa de 10 segundos para não exceder o limite da API (Free Tier)...")
            time.sleep(10)
    
    logging.info("--- Processamento Concluído com Sucesso! ---")
    logging.info("Seu banco de dados vetorial está pronto para ser consultado.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Processa um arquivo PDF.")
    parser.add_argument("--pdf", default=DEFAULT_PDF_FILE_PATH, help="Caminho para o arquivo PDF.")
    parser.add_argument("--db", default=DEFAULT_PERSIST_DIRECTORY, help="Caminho para o diretório do ChromaDB.")
    args = parser.parse_args()

    processar_e_salvar_documentos(pdf_path=args.pdf, persist_directory=args.db)