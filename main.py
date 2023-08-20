from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import apikey
import os


app = Flask(__name__)
CORS(app)
api = Api(app)


def customChatInstance(file, userInput, language):
    os.environ["OPENAI_API_KEY"] = apikey.OPENAIKEY

    loader = PyPDFLoader(file)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
    all_splits = text_splitter.split_documents(data)
    vectorstore = Chroma.from_documents(
        documents=all_splits, embedding=OpenAIEmbeddings()
    )

    input = userInput
    language = language
    question = f"{input}; Give the answer in {language}"

    template = """
    Use the context to answer the question. 
    If the context is a textbook, 
    then give some relevant examples to the question. 
    Do this specifially based on the data provided. 
    If the data does not provide an answer, 
    then you can use some of your own knowledge to answer. 
    Do not make up answers.
    {context}
    Question: {question}
    """

    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.5)

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    result = qa_chain({"query": question})

    return result


class MainLink(Resource):
    @cross_origin()
    def options(self):
        return {"Allow": "POST, GET"}, 200

    def post(self):
        data = request.get_json()  # Retrieve JSON data from the request body
        input = data.get("input")
        file = data.get("file")
        language = data.get("language")

        output = customChatInstance(file, input, language)

        return output

    def get(self):
        return {"Hello": "Server is Running!"}


api.add_resource(MainLink, "/")

if __name__ == "__main__":
    app.run()