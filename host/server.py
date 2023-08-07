# Flask app
from flask import Flask, request, jsonify
from tackle import generate_response
from prompt import prompt_for_classfication
from image import image_gen, ImageGenerator
import re
from llm import llm_davinci

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


@app.route('/file_uploader', methods=['POST'])
def file_uploader():
    data = request.get_json()
    purpose = data["purpose"]
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
        print("*************************")
        print(category)
        print("*************************")
        if category == '1':
            print("image related")
            response, image, state = image_gen(data, state, generator)
        elif category == "2":
            print("code related")
            # going to be implement it later
            response = "We don't have the code related response funtion yet"
            image = 'NULL'
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
    app.run()
