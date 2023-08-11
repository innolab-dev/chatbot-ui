# Flask app
import os
from flask import Flask, redirect, url_for, request, jsonify
from tackle import generate_response
from prompt import prompt_for_classfication, prompt_file_uploader_routing
from image import image_gen, ImageGenerator
import re
import json
from urllib.parse import parse_qs
from llm import llm_davinci
from power_automate import send_email
from memory import memory
from Chromadb import DB
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# set global state here first, later may just pass it as a input/output messsage with the ui
state = None

# need to change the history declartion here later
# memory, mongo = memory("test-session")
# usage
generator = ImageGenerator()


database = DB("database")


@app.route('/uploads', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Get the filename
    filename = file.filename
    folder = './uploads'
    # Save file
    app.config['UPLOAD_FOLDER'] = folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # response = database.upload(folder + "/" + filename)
    response = {"message": "File uploaded successfully"}
    return response


@app.route('/file_uploader', methods=['POST', 'GET'])
def file_uploader():
    if request.is_json:
        # direct access
        data = request.get_json()
    else:
        # redirect access
        data = request.args
    purpose = data.get('purpose')
    if purpose == "search":
        query = data["query"]
        response = database.search(query)
    elif purpose == "delete":
        id = data["id"]
        response = database.delete(id)
    elif purpose == "list":
        response = database.list_documents()
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
    # data = request.get_json()
    if request.is_json:
        data = request.get_json()
        # print("model", data.get('model'))
        # print("systemPrompt", data.get('systemPrompt'))
        # print("temperature", data.get('temperature'))
        # print("messages", data.get('messages'))
        # print("message", data.get('message'))
        prompt = data.get('message')['content']
        # print("id", data.get('conversationID'))
        # print("key", data.get('key'))
    else:
        query_string = request.query_string
        params = parse_qs(query_string)
        params = {k.decode(): v[0].decode() for k, v in params.items()}
        prompt = params['Prompt']

    print("state is :", state)
    if state == None:
        llm_model_selection = data["model"]['id']
        llm_model_selection = "gpt35"  # hard code for now
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
            return redirect(url_for('file_uploader', purpose=red.get("purpose"), query=red.get("query"), id=red.get("id")))
        else:
            print("general answering")
            # Run response generation code
            conversationID = data.get('conversationID')
            memory, mongo = memory(conversationID)
            temperature = data.get('temperature')
            response = generate_response(
                prompt, memory, mongo, temperature, llm_model_selection)
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
    app.run(host="219.79.203.190")
