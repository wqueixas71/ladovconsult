import streamlit as st
import google.generativeai as genai

# Configuração da API do Gemini usando Streamlit Secrets
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Configura o título e o ícone da página
st.set_page_config(page_title="Chatbot Sommelier", page_icon="🍷")

st.title("🍇 Olá! Bem vindo ao Lado V")
st.caption("Sou seu assistente virtual especializado em vinhos.")

# Função para converter o formato de mensagem do Streamlit para o do Gemini
def convert_messages_to_history(messages):
    """
    Converts Streamlit's message format to Gemini's chat history format.
    The Gemini model expects a list of dictionaries with 'role' and 'parts'.
    """
    history = []
    for message in messages:
        # Gemini usa "model" para o assistente
        role = "model" if message["role"] == "assistant" else "user"
        history.append({"role": role, "parts": [message["content"]]})
    return history

@st.cache_resource(show_spinner=False)
def get_model():
    """
    Função para inicializar e armazenar o modelo do Gemini.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "Você é um sommelier e assistente virtual de uma loja de vinhos. "
            "Seu único objetivo é ajudar os clientes a escolher vinhos, "
            "dar sugestões de harmonização e responder a perguntas sobre "
            "vinhos, uvas e regiões vinícolas. "
            "Se o usuário perguntar algo que não seja sobre vinhos, "
            "você deve responder de forma educada e respeitosa. "
            "Exemplo: 'Essa é uma ótima pergunta, mas meu foco é apenas "
            "em vinhos. Como posso te ajudar a encontrar a garrafa perfeita?'"
        )
    )
    return model

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pergunte-me algo sobre vinhos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_model = get_model()
        
        # Converte o histórico da sessão para o formato que a API do Gemini entende
        history_for_gemini = convert_messages_to_history(st.session_state.messages)
        
        # Inicia a sessão de chat com o histórico convertido
        chat_session = chat_model.start_chat(history=history_for_gemini)
        
        try:
            # Envia a última mensagem do usuário para o chat
            response = chat_session.send_message(prompt)
            st.markdown(response.text)
            
            # Adiciona a resposta do assistente ao histórico da sessão
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except genai.types.generation_types.BlockedPromptException as e:
            # Captura a exceção se a resposta for bloqueada por segurança
            st.warning("Desculpe, a sua solicitação foi bloqueada por razões de segurança. Tente uma pergunta diferente.")
            # Remove a última mensagem para não salvar o prompt bloqueado
            st.session_state.messages.pop()
