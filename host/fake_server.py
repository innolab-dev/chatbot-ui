# Flask app
import os
from flask import Flask, request, jsonify

from memory import memory
from Chromadb import DB
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# set global state here first, later may just pass it as a input/output messsage with the ui
state = None

# need to change the history declartion here later


# may change here later.


@app.route('/file_uploader', methods=['POST'])
def file_uploader():
    # if request.is_json:
    #     print("json")
    #     print(request.files['files'])
    #     data = request.get_json()
    # else:
    #     data = request.args
    # # purpose = data.get('purpose')
    # print(data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.get_json()
    # purpose = data['dick']
    # print(purpose)
    print(data)
    # print(data["dick"])
    return data
    if purpose == "upload":
        file = data["files"]
        print(file)
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


@app.route('/testing', methods=['POST'])
def testing():
    data = request.get_json()

    print("model", data.get('model'))
    print("systemPrompt", data.get('systemPrompt'))
    print("temperature", data.get('temperature'))
    print("messages", data.get('messages'))
    print("message", data.get('message'))
    print("id", data.get('id'))
    print("key", data.get('key'))

    result = {
        'text': "DLLM",
        'image': None
    }
    return jsonify(result)


@app.route('/uploads', methods=['POST'])
def upload_file():
    file = request.files['file']

    # Save file
    # Get the filename
    filename = file.filename

    # Change the filename
    app.config['UPLOAD_FOLDER'] = './uploads'
    # Save the file with new name
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return {"message": "File uploaded successfully"}


if __name__ == '__main__':
    app.run(host="219.78.93.165", port=1111)
