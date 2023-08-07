# Provide the connection string to connect to the MongoDB database


from langchain.memory import MongoDBChatMessageHistory
connection_string = "mongodb+srv://projectvpn39:MVd6se17m8KgjLwC@cluster0.bdqojht.mongodb.net/?retryWrites=true&w=majority"


message_history = MongoDBChatMessageHistory(

    connection_string=connection_string, session_id="test-session"

)


message_history.add_user_message("hi!")


message_history.add_ai_message("whats up?")
