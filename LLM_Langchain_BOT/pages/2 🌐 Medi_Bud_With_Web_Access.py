import utils
import streamlit as st

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool

st.set_page_config(page_title="Medi Bud RAG Net", page_icon="🌎")
st.header('AI Med bot with Web Access')
st.write('Equipped with internet access, enables users to ask questions about recent events')
st.write('[![View Source Code](https://img.shields.io/badge/View%20Source%20Code-%2300A7E1.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/XAheli/Medi_Bud)')
st.caption("Try to ask those things which are small to answer.. since this is just a prototype")
st.caption("Fun Fact: Apart from medical queries... It can solve Maths also...Try it! ")
class InternetChatbot:

    def __init__(self):
        utils.sync_st_session()
        self.llm = utils.configure_llm()

    # @st.cache_resource(show_spinner='Connecting..')
    def setup_agent(_self):
        # Define tool
        ddg_search = DuckDuckGoSearchRun()
        tools = [
            Tool(
                name="DuckDuckGoSearch",
                func=ddg_search.run,
                description="Useful for when you need to answer questions about current events. You should ask targeted questions",
            )
        ]

        # Get the prompt - can modify this
        prompt = hub.pull("hwchase17/react-chat")

        # Setup LLM and Agent
        memory = ConversationBufferMemory(memory_key="chat_history")
        agent = create_react_agent(_self.llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=False)
        return agent_executor, memory

    @utils.enable_chat_history
    def main(self):
        agent_executor, memory = self.setup_agent()
        user_query = st.chat_input(placeholder="Ask me anything!")
        try:
            if user_query:
                utils.display_msg(user_query, 'user')
                with st.chat_message("assistant"):
                    st_cb = StreamlitCallbackHandler(st.container())
                    result = agent_executor.invoke(
                        {"input": user_query, "chat_history": memory.chat_memory.messages},
                        {"callbacks": [st_cb]}
                    )
                    response = result["output"]
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.write(response)
                    utils.print_qa(InternetChatbot, user_query, response)
        except:
            st.warning("Some error occured due to large requests fetching... please try something less complex or simpler for the model to react")
            #utils.print_qa(InternetChatbot, user_query, response)
                

if __name__ == "__main__":
    try:
        obj = InternetChatbot()
        obj.main()
    except Exception as e:
        st.warning("Section Under Maintenance,Comeback Later!Check our Prescription decoder section until that!")
        st.info(f"Error details: {e}")
