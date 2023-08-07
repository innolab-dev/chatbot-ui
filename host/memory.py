from langchain.memory import MongoDBChatMessageHistory
from langchain.memory import ConversationBufferMemory


def mongo_to_conversation(mongo):
    converstion_memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    # Set MongoaDB chat history
    converstion_memory.chat_memory.messages = mongo.messages
    return converstion_memory


connection_string = "mongodb+srv://projectvpn39:MVd6se17m8KgjLwC@cluster0.bdqojht.mongodb.net/?retryWrites=true&w=majority"


def memory(session_id):
    mongo = MongoDBChatMessageHistory(
        connection_string=connection_string, session_id=session_id
    )
    memory = mongo_to_conversation(mongo)
    return memory, mongo
