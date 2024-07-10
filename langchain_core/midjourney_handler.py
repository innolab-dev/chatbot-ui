import socket
import requests
import json


def wait_for_data(type, id_post):
    # create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 1234))
    server_socket.listen(1)

    # initialize datas to an empty dictionary
    datas = {}

    while True:
        # wait for a connection from program A
        client_socket, _ = server_socket.accept()

        # receive all data from program A
        data = ""
        while True:
            chunk = client_socket.recv(1024).decode()
            if not chunk:
                break
            data += chunk

        # close the sockets
        client_socket.close()

        datas = json.loads(data)

        if type == 'post':
            break

        if type == 'upscale' or type == 'variation' or type == 'reset':
            message_id = datas["id"]
            if message_id != id_post:
                break

    server_socket.close()
    return datas


def gen_image(prompt):
    # prompt = input("please type your wanted command of image generate: ")

    # Send the first request to trigger the imagine endpoint
    imagine_url = 'http://127.0.0.1:8062/v1/api/trigger/imagine'

    imagine_data = {
        "prompt": prompt
    }

    imagine_response = requests.post(imagine_url, json=imagine_data)

    # wait for the my_callback function to be called
    data = wait_for_data("post", 0)

    # load the JSON string into a dictionary
    # data = json.loads(data)

    # extract the values you need
    # file_name = data["attachments"][0]["filename"]
    message_id = data["id"]
    msg_hash = data["attachments"][0]["filename"].split("_")[-1].split(".")[0]
    trigger_id = data["trigger_id"]
    url = data["attachments"][0]["url"]
    proxy_url = data["attachments"][0]["proxy_url"]

    # print the extracted values
    # debug use
    # print(f"message_id: {message_id}")
    # print(f"msg_hash: {msg_hash}")
    # print(f"trigger_id: {trigger_id}")
    # print(f"url: {url}")
    # print(f"proxy_url: {proxy_url}")

    # save image
    # image_response = requests.get(url)
    # with open("Post_image.png", 'wb') as f:
    #     f.write(image_response.content)
    return message_id, msg_hash, trigger_id, url


# selection_mode = input(
#     "what you want to choose? \nupscale press \"U\" or \nvariation choose \"V\" \nor regenerate choose \"R\"\n")
# if selection_mode != 'R':
#     selection_index = input("which one you want to progress? press 1-4")

def upscale(selection_index, message_id, msg_hash, trigger_id):
    upscale_url = 'http://127.0.0.1:8062/v1/api/trigger/upscale'
    upscale_data = {
        "index": selection_index,
        "msg_id": message_id,
        "msg_hash": msg_hash,
        "trigger_id": trigger_id
    }
    upscale_response = requests.post(upscale_url, json=upscale_data)

    # wait for the my_callback function to be called
    data = wait_for_data('upscale', message_id)

    message_id = data["id"]
    msg_hash = data["attachments"][0]["filename"].split("_")[-1].split(".")[0]
    trigger_id = data["trigger_id"]
    proxy_url = data["attachments"][0]["proxy_url"]
    return message_id, msg_hash, trigger_id, proxy_url
    # upscale_response = requests.get(proxy_url)
    # with open("Upscale.png", 'wb') as f:
    #     f.write(upscale_response.content)


def variation(selection_index, message_id, msg_hash, trigger_id):
    variation_url = 'http://127.0.0.1:8062/v1/api/trigger/variation'
    variation_data = {
        "index": selection_index,
        "msg_id": message_id,
        "msg_hash": msg_hash,
        "trigger_id": trigger_id
    }
    variation_response = requests.post(variation_url, json=variation_data)

    # wait for the my_callback function to be called
    data = wait_for_data('variation', message_id)
    proxy_url = data["attachments"][0]["proxy_url"]
    # print(proxy_url)
    return message_id, msg_hash, trigger_id, proxy_url

    # variation_response = requests.get(proxy_url)
    # with open("Variation.png", 'wb') as f:
    #     f.write(variation_response.content)


def reset(message_id, msg_hash, trigger_id):
    reset_url = 'http://127.0.0.1:8062/v1/api/trigger/reset'
    reset_data = {
        "msg_id": message_id,
        "msg_hash": msg_hash,
        "trigger_id": trigger_id
    }
    reset_response = requests.post(reset_url, json=reset_data)

    # wait for the my_callback function to be called
    data = wait_for_data('reset', message_id)
    message_id = data["id"]
    msg_hash = data["attachments"][0]["filename"].split("_")[-1].split(".")[0]
    trigger_id = data["trigger_id"]
    url = data["attachments"][0]["url"]
    proxy_url = data["attachments"][0]["proxy_url"]
    return message_id, msg_hash, trigger_id, proxy_url

    # reset_response = requests.get(proxy_url)
    # with open("reset.png", 'wb') as f:
    #     f.write(reset_response.content)
