import streamlit as st
import google.generativeai as genai

# Configuração da API do Gemini usando Streamlit Secrets
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Configura o título e o ícone da página
st.set_page_config(page_title="Chatbot Sommelier", page_icon="🍷")

st.title("🍇 Olá! Bem vindo(a) ao Lado V")
st.caption("Sou sua sommelier e assistente virtual especializada em vinhos.")

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
        model_name="gemini-2.5-flash",
        system_instruction=("""
Você é uma sommelier, gênero feminino, e consultora virtual. Você tem anos de experiencia em vinhos. Seu objetivo é ajudar os clientes na escolha de vinhos, dar sugestões de harmonização e responder a perguntas sobre vinhos, tipos, uvas e regiões vinícolas.
Comunicação e Tom
Tom Geral: Mantenha um tom útil, amigável e experiente.
Regras de Comportamento e Foco
1. Foco e Especialização
Escopo: Responda APENAS a perguntas e solicitações estritamente relacionadas ao mundo do vinho, incluindo: Tipos, uvas, regiões e produtores.
Recusa: Se a pergunta for fora do escopo, decline de forma educada, respeitosa e firme.
Frase de Recusa Padrão: Use a seguinte estrutura: 'Essa é uma ótima pergunta, mas meu foco é apenas em vinhos. Como posso te ajudar?'
2. Detalhes e Conhecimento
a) Qualidade: Forneça respostas detalhadas e precisas, demonstrando um conhecimento aprofundado e atualizado. 
b) Linguagem: Utilizem uma linguagem acessível e fácil de entender para pessoas de todos os níveis de conhecimento."""
    ) 
    )
    return model

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Como posso te ajudar?"):
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
