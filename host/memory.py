from langchain.memory import MongoDBChatMessageHistory
from langchain.memory import ConversationBufferMemory


def mongo_to_conversation(mongo):
    converstion_memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    # Set MongoaDB chat history
    converstion_memory.chat_memory.messages = mongo.messages
    print(mongo.messages)
    return converstion_memory


connection_string = "mongodb+srv://projectvpn39:QZmbpXQdZr5TLoUh@cluster0.bdqojht.mongodb.net/?retryWrites=true&w=majority"


def memory(conversation_id):
    mongo = MongoDBChatMessageHistory(
        connection_string=connection_string, database_name="langchain", collection_name="chat_history", session_id=conversation_id
    )
    memory = mongo_to_conversation(mongo)
    return memory, mongo
