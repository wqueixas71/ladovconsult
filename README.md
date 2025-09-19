# 🤖 Chatbot Sommelier com Gemini e Streamlit

Um chatbot interativo feito para dar sugestões de vinhos, harmonização e responder a perguntas sobre o assunto. O projeto utiliza a API do Google Gemini para inteligência artificial e o framework Streamlit para a interface web.

## 🚀 Como Executar

Siga estas instruções para rodar o chatbot localmente na sua máquina.

### Pré-requisitos

Certifique-se de que você tem o **Python** (versão 3.8 ou superior) instalado.

As dependências do projeto são listadas no arquivo `requirements.txt`.

### Instalação

1.  Clone o repositório para sua máquina local:
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  Crie e ative um ambiente virtual (opcional, mas recomendado):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Instale as bibliotecas necessárias. As dependências estão no arquivo `requirements.txt` que você gerou:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure sua chave da API do Gemini. Crie uma pasta chamada `.streamlit` e um arquivo chamado `secrets.toml` dentro dela.

    ```toml
    # Arquivo: .streamlit/secrets.toml
    [gemini]
    api_key = "SUA_CHAVE_AQUI"
    ```

### Uso

Para rodar o chatbot, execute o seguinte comando no terminal:

```bash
streamlit run streamlit_app.py
