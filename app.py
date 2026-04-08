import streamlit as st
import requests

# 1. CONFIGURAÇÃO DA PÁGINA (Aba do browser)
# Tem de ser o primeiro comando do Streamlit!
st.set_page_config(
    page_title="Zélia",
    layout="centered"
)

# --- CSS PERSONALIZADO ---
# Usamos unsafe_allow_html para injetar CSS radical e alterar o layout padrão
st.markdown("""<style>
    /* 1. Estilos da Sidebar (Cor de fundo, etc.) */
    [data-testid="stSidebar"] {
        background-color: #e0d9f0 !important; /* Cor de fundo alfazema */
        border-right: none !important;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: black !important;
        padding-top: 1em;
        padding-left: 20px;
    }

    /* 2. Estilos do Título Principal e do Input Central */
    /* Removemos o título padrão do Streamlit */
    [data-testid="stHeader"] {
        display: none !important;
    }
    /* Estilo para o título central 'zélia' */
    .central-title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        color: black;
        margin-top: 2em;
        margin-bottom: 0.5em;
    }

    /* 3. Estilos do Chat Input (Caixa de texto centrada) */
    .stChatInputContainer {
        display: flex;
        justify-content: center;
        width: 100% !important;
        margin-top: 1em !important;
        margin-bottom: 1em !important;
    }
    .stChatInputContainer textarea {
        text-align: center; /* Centraliza o texto digitado e o placeholder */
        border: 1px solid #e0d9f0 !important; /* Borda alfazema leve */
        border-radius: 20px !important;
        width: 70% !important; /* Torna a caixa mais larga */
        color: black !important;
        background-color: transparent !important;
        font-size: 1.2em !important;
    }
    .stChatInputContainer textarea::placeholder {
        color: #555 !important;
    }
    /* Removemos o botão de envio padrão (pequena seta à direita) */
    .stChatInputContainer button[kind="primary"] {
        display: none !important;
    }
    /* Criamos um ícone de envio centralizado (seta) usando CSS */
    .stChatInputContainer::after {
        content: '→'; /* Seta de envio centralizada */
        color: #e0d9f0;
        font-size: 1.5em;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none; /* Garante que o clique vá para a caixa de texto */
        z-index: 10;
    }

    /* 4. Estilos para Mensagens */
    /* Removemos os estilos padrão de chat_message */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 0 !important;
        border: none !important;
    }
    [data-testid="stChatMessageContent"] {
        text-align: center; /* Centraliza o texto das mensagens */
        color: black !important;
        font-size: 1.1em !important;
        margin-top: 1em !important;
    }
    /* Estilo para mensagens do aluno (negrito) */
    .user-message {
        font-weight: bold;
    }
    /* Estilo para mensagens da Zélia (plain text) */
    .assistant-message {
    }

    /* 5. Estilo para o Rodapé (Footer) */
    .footer-attribution {
        text-align: center;
        color: black;
        font-size: 0.8em;
        margin-top: 4em;
    }
</style>""", unsafe_allow_html=True)

# 2. BARRA LATERAL 
with st.sidebar:
    # Conteúdo da sidebar
    st.markdown("<h1 style='font-size: 6em; font-weight: bold; margin-top: 0; color: #000; font-family: sans-serif; text-align: left;'>Z</h1>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 10px; margin-top: 1em;'><span style='font-size: 1.5em;'>+</span> <a href='#' style='color: black;'>Nova conversa</a></div>", unsafe_allow_html=True)
    st.markdown("<div style='display: flex; align-items: center; gap: 10px;'><span style='font-size: 1.5em;'>🔍</span> <a href='#' style='color: black;'>Pesquisar</a></div>", unsafe_allow_html=True)
    st.divider() # Linha de separação
    
    # Botão para limpar a memória da conversa (agora centralizado)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("🗑️ Limpar Conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun() # Atualiza o ecrã instantaneamente
    st.markdown("</div>", unsafe_allow_html=True)

# 3. CABEÇALHO PRINCIPAL 
# Usamos HTML direto com a classe central-title para estilizar
st.markdown("<h1 class='central-title'>zélia</h1>", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/perguntar"

# Inicializa o histórico se estiver vazio
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. EXIBIR MENSAGENS 
# Loop para renderizar o histórico 
for message in st.session_state.messages:
    # Usamos classes CSS diferentes para o aluno e para a Zélia
    if message["role"] == "user":
        # Pergunta do aluno: Centrada e a Negrito
        st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        # Resposta da Zélia: Centrada e em texto simples
        st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)

# 5. CAIXA DE TEXTO E ENVIO 
# Usamos st.chat_input, mas o CSS acima irá personalizá-lo para ficar centrado e minimalista
if prompt := st.chat_input("Pergunte-me algo"):
    
    # Adiciona a pergunta do aluno ao histórico e exibe-a centrado e a negrito
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

    # Chama a API e exibe a resposta da Zélia
    # O Streamlit ainda usa a classe stChatInput para capturar o input, então mantemos a lógica
    # mas o CSS garante a aparência centrada
    # Para a resposta, usamos um st.empty() centrado para carregar a resposta
    message_placeholder = st.empty()
    # Texto de carregamento centrado e minimalista
    message_placeholder.markdown("<div style='text-align: center; color: #555;'>A consultar o manual... ⏳</div>", unsafe_allow_html=True)
        
    try:
        # Envia a pergunta E o histórico
        payload = {
            "query": prompt,
            "history": st.session_state.messages
        }
        
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            resposta_ia = response.json().get("answer", "Desculpe, não consegui obter a resposta.")
            # Resposta final centrada e em texto simples
            message_placeholder.markdown(f"<div class='assistant-message'>{resposta_ia}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
        else:
            message_placeholder.markdown(f"<div style='text-align: center; color: #d9534f;'>❌ Erro na API: Status {response.status_code}</div>", unsafe_allow_html=True)
            
    except requests.exceptions.ConnectionError:
        message_placeholder.markdown("<div style='text-align: center; color: #d9534f;'>❌ Erro de ligação ao servidor FastAPI!</div>", unsafe_allow_html=True)

# 6. RODAPÉ
# Adiciona o texto de atribuição pequeno e centrado no final da página
st.markdown("<div class='footer-attribution'>Desenvolvido por Fábio Pereira</div>", unsafe_allow_html=True)