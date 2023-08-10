# Flask app
from flask import Flask, redirect, url_for, request, jsonify
from tackle import generate_response
from prompt import prompt_for_classfication, prompt_file_uploader_routing
from image import image_gen, ImageGenerator
import re
import json
from llm import llm_davinci
from power_automate import send_email
from memory import memory
from Chromadb import DB
app = Flask(__name__)

# set global state here first, later may just pass it as a input/output messsage with the ui
state = None

# need to change the history declartion here later
memory, mongo = memory("test-session")
# usage
generator = ImageGenerator()


database = DB("database")

# may change here later.


@app.route('/file_uploader', methods=['POST', 'GET'])
def file_uploader():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.args
    purpose = data.get('purpose')
    if purpose == "upload":
        file = data["files"]
        response = database.upload(file)
    elif purpose == "search":
        query = data["query"]
        response = database.search(query)
    elif purpose == "delete":
        id = data["id"]
        response = database.delete(id)
    elif purpose == "list":
        response = database.list_documents()
    elif purpose == "upload and search":
        file = data["files"]
        response = database.upload(file)
        query = data["query"]
        response = database.search(query)
    result = {
        'text': response,
        'image': None
    }
    return jsonify(result)


@app.route('/code-related', methods=['POST'])
def code():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.args
    response = "We don't have the code related response funtion yet"
    # going to be implement it later
    result = {
        'text': response,
        'image': None
    }
    return jsonify(result)


@app.route('/email-sender', methods=['POST'])
def email():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.args
    prompt = data["messages"][-1]["content"]
    response = send_email(prompt)
    result = {
        'text': response,
        'image': None
    }
    return jsonify(result)


@app.route('/chat', methods=['POST'])
def chat():
    global state
    # response = "something problem just hold up"
    data = request.get_json()

    # result = {
    #     'text': "DLLM",
    #     'image': "NULL"
    # }
    # return jsonify(result)

    # which track?
    print("state is :", state)
    if state == None:
        prompt = data["messages"][-1]["content"]
        # print(prompt_for_classfication.format(prompt=prompt))
        s = llm_davinci(prompt_for_classfication.format(prompt=prompt))
        # Extract number
        match = re.search(r'(\d)', s)
        if match:
            category = match.group(1)
        # print("*************************")
        # print(category)
        # print("*************************")
        if category == '1':
            print("image related")
            response, image, state = image_gen(data, state, generator)
        elif category == "2":
            print("code related")
            # going to be implement it later
            response = "We don't have the code related response funtion yet"
            image = 'NULL'
        elif category == "3":
            print("email sender")
            response = send_email(prompt)
            image = 'NULL'
        elif category == "4":
            print("database related")
            # p = prompt_file_uploader_routing.format(prompt=prompt)
            res = llm_davinci(prompt_file_uploader_routing +
                              f"Current Prompt = {prompt} Ans:")
            red = json.loads(res)
            # data.get('purpose')
            return redirect(url_for('file_uploader', purpose=red.get("purpose"), query=red.get("query"), files=red.get("file_path"), id=red.get("id")))
        else:
            print("general answering")
            # Run response generation code
            response = generate_response(data, memory, mongo)
            image = 'NULL'

    elif state == "image":
        print("image follow up")
        response, image, state = image_gen(data, state, generator)

    result = {
        'text': response,
        'image': image
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="219.78.93.165")
