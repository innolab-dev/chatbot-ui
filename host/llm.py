from langchain.chat_models import ChatVertexAI
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
import os
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI


os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
os.environ["OPENAI_API_BASE"] = "https://pocsc.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "f96c629ba6874b2aaa7569acfea2162c"
os.environ["GOOGLE_CSE_ID"] = "8541de27511e045ba"
os.environ["GOOGLE_API_KEY"] = "AIzaSyBaI5KQDKn08A47v8JI0-SXPBaMQJOxrsQ"


llm_azure_gpt35 = AzureChatOpenAI(
    streaming=True,
    # callbacks=[StreamingCallbackHandler()],
    temperature=0,
    deployment_name="gpt35",
    model_name="gpt-35-turbo"
)
# <- use this one, but not gpt35, for some simple task
llm_davinci = AzureOpenAI(deployment_name='text-davinci-003')


# data vector storage
# for storing data, we can use different method, one of the method is using pinecone, which is the online resourse
# May also use the chroma for local storage
PINECONE_API_KEY = "1da3ed2f-1c22-48b1-84f9-18d254b222ee"
PINECONE_ENV = "us-west1-gcp-free"
# we need to use the embedding model here
pinecone.init(
    api_key="1da3ed2f-1c22-48b1-84f9-18d254b222ee",
    environment="us-west1-gcp-free"
)
embeddings = OpenAIEmbeddings(deployment="text-embedding-ada-002")
doc_db = Pinecone.from_existing_index('langchain-demo', embeddings)

internaL_db = RetrievalQA.from_chain_type(
    llm=llm_azure_gpt35, chain_type="stuff", retriever=doc_db.as_retriever()
)


bison_chat = ChatVertexAI(model_name="chat-bison@001", max_output_tokens=512)
codey = ChatVertexAI(model_name='codechat-bison@001', max_output_tokens=512)
