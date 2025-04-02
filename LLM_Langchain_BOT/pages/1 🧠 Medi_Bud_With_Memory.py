import os
import utils
import streamlit as st
from streaming import StreamHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, ConversationChain
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

st.set_page_config(page_title="Medi Bud Chatbot", page_icon="⚕️")
st.header('AI-Powered Virtual Health Assistant')
st.write('Providing preliminary consultations and answering health-related queries for patients in remote areas.')
st.write('[![View Source Code](https://img.shields.io/badge/View%20Source%20Code-%2300A7E1.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/XAheli/Medi_Bud)')
st.caption("Kindy keep the document size less than 1.5MB")

class MedicalChatbot:

    def __init__(self):
        utils.sync_st_session()
        self.llm = utils.configure_llm()
        self.embedding_model = utils.configure_embedding_model()

    def save_file(self, file):
        folder = 'tmp'
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = f'./{folder}/{file.name}'
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())
        return file_path

    def setup_qa_chain(self, uploaded_files):
        # Load medical documents
        docs = []
        for file in uploaded_files:
            file_path = self.save_file(file)
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())
        
        # Split documents and store in vector db
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)
        vectordb = DocArrayInMemorySearch.from_documents(splits, self.embedding_model)

        # Define retriever
        retriever = vectordb.as_retriever(
            search_type='mmr',
            search_kwargs={'k': 2, 'fetch_k': 4}
        )

        # Setup memory for contextual conversation        
        memory = ConversationBufferMemory(
            memory_key='chat_history',  # Use 'chat_history' for PDF-based context
            output_key='answer',  # Specify 'answer' as the output key for memory
            return_messages=True
        )

        # Setup LLM and QA chain with document retrieval
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=False,
            output_key='answer'  # Explicitly define 'answer' as the output key
        )
        return qa_chain

    def setup_basic_chain(self):
        # Setup a simple conversation chain without document retrieval
        try:
            memory = ConversationBufferMemory(
                memory_key="history",  # Use 'history' for normal conversation without documents
                return_messages=True
            )
            basic_chain = ConversationChain(
                llm=self.llm,
                memory=memory,
                verbose=False
            )
            return basic_chain
        except:
            st.write("Some error has happened")

    @utils.enable_chat_history
    def main(self):
        # User Inputs
        uploaded_files = st.sidebar.file_uploader(
            label='Upload Medical PDF files (optional)', 
            type=['pdf'], 
            accept_multiple_files=True
        )

        # Capture user query
        user_query = st.chat_input(placeholder="Ask me about your health concerns...")

        try:

            # Process based on user input and uploaded files
            if user_query:
                utils.display_msg(user_query, 'user')
                
                # If documents are uploaded, use QA chain (PDF Mode)
                if uploaded_files:
                    with st.spinner('Analyzing documents...'):
                        qa_chain = self.setup_qa_chain(uploaded_files)
                        with st.chat_message("assistant"):
                            st_cb = StreamHandler(st.empty())
                            result = qa_chain.invoke(
                                {"question": user_query, "chat_history": []},  # Pass 'chat_history' for document-based QA
                                {"callbacks": [st_cb]}
                            )
                            response = result["answer"]
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            utils.print_qa(MedicalChatbot, user_query, response)
    
                            # Show document references
                            for idx, doc in enumerate(result['source_documents'], 1):
                                filename = os.path.basename(doc.metadata['source'])
                                page_num = doc.metadata['page']
                                ref_title = f":blue[Reference {idx}: *{filename} - page.{page_num}*]"
                                with st.popover(ref_title):
                                    st.caption(doc.page_content)
                else:
                    # If no documents are uploaded, use basic chain (Basic Mode)
                    basic_chain = self.setup_basic_chain()
                    with st.chat_message("assistant"):
                        st_cb = StreamHandler(st.empty())
                        result = basic_chain.invoke(
                            {"input": user_query},  # Use 'input' for simple conversation
                            {"callbacks": [st_cb]}
                        )
                        response = result["response"]
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        utils.print_qa(MedicalChatbot, user_query, response)
    
                    # Provide guidance based on health query
                    if "emergency" in user_query.lower() or "urgent" in user_query.lower():
                        st.warning("⚠️ Based on your query, we recommend seeking immediate medical assistance.")
        except:
            st.warning("Some error might have happened due to the size of the files, reduce the file size and try again")

if __name__ == "__main__":
    # obj = MedicalChatbot()
    # obj.main()
    try:
        obj = MedicalChatbot()
        obj.main()
    except Exception as e:
        st.warning("Section Under Maintenance,Comeback Later!Check our Prescription decoder section until that!")
        st.info(f"Error details: {e}")

    
