# Flask app
import os
from flask import Flask, redirect, url_for, request, jsonify
from tackle import generate_response, code_gen
from prompt import prompt_for_classfication, prompt_file_uploader_routing
from image import image_gen, ImageGenerator
import re
import json
from urllib.parse import parse_qs
from llm import llm_davinci, codey
from power_automate import send_email
from memory import memory
from Chromadb import DBManager
from email_class import email_class
from flask_cors import CORS
app = Flask(__name__)  # build Application object
CORS(app)


# need to change the history declartion here later
# memory, mongo = memory("test-session")
# usage
generator = ImageGenerator()  # image class, but it is shared now


@app.route('/uploads', methods=['POST'])
def upload_file():
    file = request.files['file']
    email = request.form['email']
    email_class.set_email(email)  # set email
    # Get the filename
    filename = file.filename
    folder = './uploads'
    # Save file
    app.config['UPLOAD_FOLDER'] = folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Upload file to database
    response = DBManager.get_or_setup().upload(folder + "/" + filename)
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
    if purpose == "delete":
        id = data["id"]
        print("id: ", id)
        response = DBManager.get_or_setup().delete(id)
    elif purpose == "list":
        response = DBManager.get_or_setup().list_documents()
    result = {
        'text': response,
        'image': 'NULL'
    }
    return jsonify(result)


@app.route('/chat', methods=['POST'])
def chat():
    if request.is_json:  # chatbot-ui
        data = request.get_json()
        prompt = data.get('message')['content']
        llm_model_selection = data["model"]['id']
        conversationID = data.get('conversationID')
        temperature = data.get('temperature')
        user_email = data.get('userEmail')
        email_class.set_email(user_email)  # set email
    else:  # teams
        query_string = request.query_string
        params = parse_qs(query_string)
        params = {k.decode(): v[0].decode() for k, v in params.items()}
        email_class.set_email(params['userEmail'])  # set email
        prompt = params['Prompt']
        llm_model_selection = "gpt35"
        temperature = 0.5
        conversationID = params['conversationID']

    image = 'NULL'
    s = llm_davinci(prompt_for_classfication.format(prompt=prompt))
    # Extract number
    match = re.search(r'(\d)', s)
    if match:
        category = match.group(1)
        if category == '1':
            print("image related")
            response, image = image_gen(prompt, generator)
        elif category == "2":
            print("code related")
            mem, mongo = memory(conversationID)
            llm_model_selection = 'codey'
            response = code_gen(prompt)
        elif category == "3":
            print("email sender")
            response = send_email(prompt)
        elif category == "4":
            print("database related")
            res = llm_davinci(prompt_file_uploader_routing +
                              f"Current Prompt = {prompt} Ans:")
            red = json.loads(res)
            return redirect(url_for('file_uploader', purpose=red.get("purpose"), id=red.get("file_id")))
        else:
            print("general answering")  # life pal function include here
            # Run response generation code
            mem, mongo = memory(conversationID)
            response = generate_response(  # tackle.py
                prompt, mem, mongo, temperature, llm_model_selection)
    else:
        response = "I don't understand what you are saying"
    result = {
        'text': response,
        'image': image
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="localhost")  # deploy on server