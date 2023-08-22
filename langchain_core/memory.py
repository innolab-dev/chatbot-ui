from langchain.memory import MongoDBChatMessageHistory
from langchain.memory import ConversationSummaryBufferMemory
from llm import llm_davinci


def mongo_to_conversation(mongo):
    conversation_memory = ConversationSummaryBufferMemory(
        memory_key="chat_history", llm=llm_davinci, max_token_limit=100)
    # Set MongoaDB chat history
    conversation_memory.chat_memory.messages = mongo.messages
    # print(mongo.messages)
    return conversation_memory


connection_string = "mongodb+srv://projectvpn39:kDir8fgavrwmXhUN@cluster0.bdqojht.mongodb.net/?retryWrites=true&w=majority"


def memory(conversation_id):
    mongo = MongoDBChatMessageHistory(
        connection_string=connection_string, database_name="langchain", collection_name="chat_history", session_id=conversation_id
    )
    memory = mongo_to_conversation(mongo)
    return memory, mongo
