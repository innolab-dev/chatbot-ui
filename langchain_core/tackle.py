import requests
import json
from langchain.agents import load_tools
from langchain.chains import LLMMathChain
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents import Tool
from Chromadb import DBManager
from email_class import email_class
# from power_automate import send_email
from llm import llm_azure_gpt35, bison_chat, codey, llm_Vicuna

# from llm import internaL_db
from langchain import PromptTemplate, LLMChain

from pymongo import MongoClient

# for life_pal part, please refer to life_pal.ipynb to get understand how they work


def get_client_info(input):
    # input is not used, just for the function to work
    # Replace the placeholder values with your actual MongoDB connection details
    client = MongoClient(
        "mongodb+srv://projectvpn39:kDir8fgavrwmXhUN@cluster0.bdqojht.mongodb.net/?retryWrites=true&w=majority")
    db = client["langchain"]
    collection = db["userinfos"]
    client_info = collection.find_one(
        {"email": email_class.get_email()})
    client_info_str = "\n".join(
        [f"- {k}: {v}" for k, v in client_info.items()])
    return client_info_str


def get_products_info_according_to_name(prdouct_name):
    client = MongoClient(
        "mongodb+srv://projectvpn39:kDir8fgavrwmXhUN@cluster0.bdqojht.mongodb.net/?retryWrites=true&w=majority")
    db = client["langchain"]
    collection = db["products"]
    client_info = collection.find_one({"product_name": prdouct_name})
    if client_info is not None:
        client_info_str = "\n".join(
            [f"- {k}: {v}" for k, v in client_info.items()])
    else:
        client_info_str = "No such product"
    return client_info_str


def get_products_info_according_to_category(category):
    client = MongoClient(
        "mongodb+srv://projectvpn39:kDir8fgavrwmXhUN@cluster0.bdqojht.mongodb.net/?retryWrites=true&w=majority")
    db = client["langchain"]
    collection = db["products"]
    client_info = collection.find(
        {"interest": category}).limit(3)
    product_info_str = ""
    for i in client_info:
        # product_info_str += f"\nProduct {i}:\n"
        product_info_str += "\n".join([f"- {k}: {v}" for k, v in i.items()])
    return product_info_str


llm_math_chain = LLMMathChain(llm=llm_azure_gpt35)
wiki_tools = load_tools(["wikipedia"], llm=llm_azure_gpt35)
tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about maths, but not anything else",
        return_direct=True,  # help you to correct the prompt
    ),
    # Tool( #pinecone use, not use now
    #     name="Internal Database",
    #     description="useful for when you need to answer questions about alphabet company annual report",
    #     func=internaL_db.run,
    # ),
    Tool(
        name="Document Database",
        description="Use for when you want to answer the question from the documents that uploaded by the user",
        func=DBManager.get_or_setup().search,
        # func=databasefunc("email").search,
    ),
    Tool(
        name="Client information",
        func=get_client_info,
        description="Use this function to get the client information",
        # return_direct=True,  # help you to correct the prompt
    ),
    Tool(
        name="Get Product information based on category",
        description="Our company have 5 category of item, please choose one of them, and I will give you the top 3 products in that category, and they are Beauty, Food, Health, Kid and Pet, Travel. Please input the exact word of category as input, like 'Health",
        func=get_products_info_according_to_category,
    ),
    Tool(
        name="Get Product information based on product name",
        description="You can search for a particular product name, and I will give you the information of that product, just need to make sure the product name need to be exactly the same as the one show in the tool above",
        func=get_products_info_according_to_name,
    ),
]


tools.append(wiki_tools[0])
google_tools = load_tools(["google-search"])
# tools[0].description = "This tool allows you to search the web using the Google Search API. Useful for when you need to answer questions about current events"
tools.append(google_tools[0])


# for google chat bison/ codey use, to prevent output paarse error
def _handle_error(error) -> str:
    print(str(error)[:1024])
    return str(error)[:1024]


def generate_response(prompt, memory, mogodb, temperature, llm_model_selection):

    mogodb.add_user_message(prompt)  # add user message to mongodb
    print(llm_model_selection)
    if llm_model_selection == "gpt35" or llm_model_selection == 'gpt4':
        llm = llm_azure_gpt35  # now default setting, will change it later
        llm.temperature = temperature
        agent_chain = initialize_agent(
            tools, llm, agent=AgentType.LIFE_PAL_SELF_DEFINE_AGENT, verbose=True, memory=memory)
    elif llm_model_selection == "Vicuna":
        llm = llm_Vicuna  # now default setting, will change it later
        llm.temperature = temperature
        agent_chain = initialize_agent(
            tools, llm, agent=AgentType.LIFE_PAL_SELF_DEFINE_AGENT, verbose=True, memory=memory)
    elif llm_model_selection == "google-chatbison" or 'codey':
        if llm_model_selection == "codey":
            llm = codey
        else:
            llm = bison_chat
        llm.temperature = temperature
        agent_chain = initialize_agent(tools, llm, agent=AgentType.LIFE_PAL_SELF_DEFINE_AGENT,
                                       verbose=True, memory=memory, handle_parsing_errors=_handle_error, max_iterations=2)
    response = agent_chain.run(input=prompt)
    mogodb.add_ai_message(response)  # add ai message to mongodb
    response += "\n\nMessage generate by: " + llm_model_selection
    return response


def code_gen(prompt):
    template = """Question: {question}

    Let's think it step by step. And return the answer in MarkDown format"""

    promptTemplate = PromptTemplate(
        template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=promptTemplate, llm=codey)
    s = llm_chain.run(prompt)
    return s
