from flask import Flask, request
from model import Model
import os

app = Flask(__name__)
txt_file_path = 'context.txt'
chatBot = None

class Model:
    def __init__(self, txt_file_path):
        self.txt_file_path = txt_file_path
        self.conversation_chain = self.create_conversation_chain()

    def data(self):
        loader = TextLoader(file_path=self.txt_file_path, encoding="utf-8")
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

def main():
    global chatBot  
    chatBot = Model(txt_file_path)

@app.route("/")
def home():
    return "Chatbot is running!"

@app.route("/internal/test_env")
def test_env():
    return os.getenv("TEST_ENV")

@app.route("/internal/query")
def query():
    query = request.args.get('question')
    return f'Q: {query}'

if __name__ == "__main__":
    main()
    app.run(debug=True)  
