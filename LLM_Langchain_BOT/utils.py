import os
import openai
import streamlit as st
from datetime import datetime
from streamlit.logger import get_logger
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

logger = get_logger('Langchain-Chatbot')

from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()

#decorator
def enable_chat_history(func):
    if os.getenv("OPENAI_API_KEY"):

        # to clear chat history after swtching chatbot
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        # to show chat history on ui
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I solve your medical queries?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def choose_custom_openai_key():
    openai_api_key = st.sidebar.text_input(
        label="OpenAI API Key",
        type="password",
        placeholder="sk-...",
        key="SELECTED_OPENAI_API_KEY"
        )
    if not openai_api_key:
        st.error("Please add your OpenAI API key to continue.")
        st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")
        st.stop()

    model = "gpt-4o-mini"
    try:
        client = openai.OpenAI(api_key=openai_api_key)
        available_models = [{"id": i.id, "created":datetime.fromtimestamp(i.created)} for i in client.models.list() if str(i.id).startswith("gpt")]
        available_models = sorted(available_models, key=lambda x: x["created"])
        available_models = [i["id"] for i in available_models]

        model = st.sidebar.selectbox(
            label="Model",
            options=available_models,
            key="SELECTED_OPENAI_MODEL"
        )
    except openai.AuthenticationError as e:
        st.error(e.body["message"])
        st.stop()
    except Exception as e:
        print(e)
        st.error("Something went wrong. Please try again later.")
        st.stop()
    return model, openai_api_key

def configure_llm():
    available_llms = ["gpt-4o-mini","llama3.2:3b","gemini","use your openai api key"]
    #available_llms = ["gpt-4o-mini","gemini","use your openai api key"]
    llm_opt = st.sidebar.radio(
        label="LLM",
        options=available_llms,
        key="SELECTED_LLM"
        )

    # if llm_opt == "llama3.1:8b":
        # llm = ChatOllama(model="llama3.1", base_url=os.getenv["OLLAMA_ENDPOINT"])
    if llm_opt == "llama3.2:3b":
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True, api_key=os.getenv("OLLAMA_ENDPOINT_KEY"))
    elif llm_opt == "gpt-4o-mini":
        #llm = ChatOpenAI(model_name=llm_opt, temperature=0, streaming=True, api_key=os.getenv["OPENAI_API_KEY"])
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True, api_key=os.getenv("OPENAI_API_KEY"))
    elif llm_opt == "gemini":
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True, api_key=os.getenv("GEMINI_API_KEY"))
    else:
        model, openai_api_key = choose_custom_openai_key()
        llm = ChatOpenAI(model_name=model, temperature=0, streaming=True, api_key=openai_api_key)
    return llm

def print_qa(cls, question, answer):
    log_str = "\nUsecase: {}\nQuestion: {}\nAnswer: {}\n" + "------"*10
    logger.info(log_str.format(cls.__name__, question, answer))

@st.cache_resource
def configure_embedding_model():
    embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return embedding_model

def sync_st_session():
    for k, v in st.session_state.items():
        st.session_state[k] = v
        
def get_prompt_template():
    template = f"""You are an AI-powered Virtual Health Assistant designed to provide preliminary consultations and answer health-related queries for patients in remote areas. Use the chat history and the user's question to provide a helpful, accurate, and empathetic response. If the query involves a medical emergency, always advise the user to seek immediate professional medical help."""

# Chat History:
# {chat_history}"""