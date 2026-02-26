import streamlit as st
import requests

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Zél.IA", page_icon="🎓", layout="centered")

st.title("🎓 Assistente Virtual - Zélia")
st.write("Olá! Sou a Zália, a assistente da Unijorge. Faça perguntas sobre o manual ou o calendário acadêmico e eu tentarei ajudar!")

# URL da sua API FastAPI (que está rodando no outro terminal)
API_URL = "http://127.0.0.1:8000/perguntar"

# 2. INICIALIZAÇÃO DO HISTÓRICO DE CHAT
# O Streamlit recarrega a página a cada clique. Isso garante que não percamos a conversa.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens antigas na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. CAPTURA A NOVA PERGUNTA DO USUÁRIO
if prompt := st.chat_input("Ex: Quantas faltas posso ter na disciplina?"):
    
    # Adiciona a pergunta do usuário no histórico e na tela
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. CHAMA A SUA API FASTAPI (O SEU BACKEND)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Consultando o manual... ⏳")
        
        try:
            # Envia a pergunta para o seu servidor
            response = requests.post(API_URL, json={"query": prompt})
            
            if response.status_code == 200:
                # Se deu tudo certo, pega a resposta gerada pelo Gemini + RAG
                resposta_ia = response.json().get("answer", "Desculpe, não entendi a resposta da API.")
                message_placeholder.markdown(resposta_ia)
                
                # Salva a resposta da IA no histórico
                st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
            else:
                message_placeholder.markdown(f"❌ Erro na API: Status {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            message_placeholder.markdown("❌ Erro de conexão. Verifique se o servidor FastAPI (uvicorn) está rodando no outro terminal!")