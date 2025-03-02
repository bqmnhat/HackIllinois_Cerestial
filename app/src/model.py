from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
import asyncio

import os

class Model:
    def __init__(self):
        self.context_path = os.getenv("CONTEXT_PATH")
        self.conversation_chain = self.create_conversation_chain()

    def data(self):
        loader = TextLoader(file_path=self.context_path, encoding="utf-8")
        data = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(data)

    def vectorstore(self):
        embeddings = OpenAIEmbeddings()
        return FAISS.from_documents(self.data(), embedding=embeddings)

    def memory(self):
        return ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    def llm(self):
        return ChatOpenAI(temperature=0.7, model_name="gpt-4o")
    
    async def get_messages_as_str(self):
        return await self.memory().abuffer_as_str()
    
    def create_conversation_chain(self):
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm(),
            chain_type="stuff",
            retriever=self.vectorstore().as_retriever(),
            memory=self.memory()
        )

    def ask(self, query):
        result = self.conversation_chain({"question": query}) 
        return result["answer"]   