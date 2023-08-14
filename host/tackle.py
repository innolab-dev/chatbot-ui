from langchain.agents import load_tools
from langchain.chains import LLMMathChain
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents import Tool

# from power_automate import send_email
from llm import llm_azure_gpt35, bison_chat, codey

from llm import internaL_db


llm_math_chain = LLMMathChain(llm=llm_azure_gpt35)
toolss = load_tools(["wikipedia"], llm=llm_azure_gpt35)
tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about maths, but not anything else",
        return_direct=True,  # help you to correct the prompt
    ),
    Tool(
        name="Internal Database",
        description="useful for when you need to answer questions about alphabet company annual report",
        func=internaL_db.run,
    ),
    # Tool(
    #     name="Send Email",
    #     func=send_email,
    #     description=""""
    #     Useful for sending the email, please just send what is the intention of the email, and who is the target to send
    #     """
    # ),
]


tools.append(toolss[0])
toolls = load_tools(["google-search"])
# tools[0].description = "This tool allows you to search the web using the Google Search API. Useful for when you need to answer questions about current events"
tools.append(toolls[0])


# def generate_response(data, memory):
#     # {'model': {'id': 'Vicuna', 'name': 'Vicuna', 'maxLength': 96000, 'tokenLimit': 32768}, 'systemPrompt': "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.", 'temperature': 0.7, 'key': '', 'messages': [{'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'Hello! How can I assist you today?'}, {'role': 'user', 'content': 'hello'}]}
#     # print(data)
#     agent_chain = initialize_agent(
#         tools, llm_azure_gpt35, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
#     prompt = data["messages"][-1]["content"]
#     response = agent_chain.run(input=prompt)
#     # print(prompt)
#     return response

def _handle_error(error) -> str:
    return str(error)[:1024]


def generate_response(prompt, memory, mogodb, temperature, llm_model_selection):
    # {'model': {'id': 'Vicuna', 'name': 'Vicuna', 'maxLength': 96000, 'tokenLimit': 32768}, 'systemPrompt': "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.", 'temperature': 0.7, 'key': '', 'messages': [{'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'Hello! How can I assist you today?'}, {'role': 'user', 'content': 'hello'}]}
    # print(data)
    # prompt = data["messages"][-1]["content"]
    mogodb.add_user_message(prompt)
    if llm_model_selection == "gpt35":
        llm = llm_azure_gpt35  # now default setting, will change it later
        llm.temperature = temperature
        agent_chain = initialize_agent(
            tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    elif llm_model_selection == "google-chatbison" or 'codey':
        if llm_model_selection == "codey":
            llm = codey
        else:
            llm = bison_chat
        llm.temperature = temperature
        agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                       verbose=True, memory=memory, handle_parsing_errors=_handle_error, max_iterations=2)
    response = agent_chain.run(input=prompt)
    mogodb.add_ai_message(response)
    return response
