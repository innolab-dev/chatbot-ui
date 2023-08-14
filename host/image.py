# image_generator.py
from prompt import prompt_for_image_description, prompt_for_image_modified, prompt_use_in_image, Prompt_template
from midjourney_handler import gen_image, upscale, reset, variation
from llm import llm_davinci
import json


class ImageGenerator:

    def __init__(self):  # in main funtion
        self.image_url = []
        self.message_id = []
        self.msg_hash = []
        self.trigger_id = []
        self.prompt = ""

    def classify_prompt(self, prompt):
        # Classify prompt
        self.prompt = llm_davinci(prompt_for_image_description.format(
            prompt=prompt))  # try to use llm_gpt35, but even worst

    def generate_image(self, model):
        # Generate image based on context
        if model == "stable diffusion":
            # image = generate_diffuse(prompt)
            # diffustion, need to put it in the url link, fix it later
            print("diffusion")
            image_url = "url"
            message_id = "null"
            msg_hash = "null"
            trigger_id = "null"
        elif model == "mid-journey":
            # replace the code in automate.py should be fine
            print("midjourney")
            print(self.prompt)
            message_id, msg_hash, trigger_id, image_url = gen_image(
                self.prompt)
        # Save
        self.message_id.append(message_id)
        self.msg_hash.append(msg_hash)
        self.trigger_id.append(trigger_id)
        self.image_url.append(image_url)

    def get_image_url(self):
        return self.image_url[-1]

    def modify_image(self, mode, num):  # fourth steps
        # Modify saved image
        # image_id should be extract inside the above generate_image,
        # like self.id etc
        index = int(num)
        if mode == "upscale":
            # upscale(selection_index, message_id, msg_hash, trigger_id)
            message_id, msg_hash, trigger_id, image_url = upscale(index, self.message_id[-1],
                                                                  self.msg_hash[-1], self.trigger_id[-1])
        elif mode == "variation":
            # variation(selection_index, message_id, msg_hash, trigger_id)
            message_id, msg_hash, trigger_id, image_url = variation(index, self.message_id[-1],
                                                                    self.msg_hash[-1], self.trigger_id[-1])
        else:
            # reset(message_id, msg_hash, trigger_id)
            message_id, msg_hash, trigger_id, image_url = reset(
                self.message_id[-1], self.msg_hash[-1], self.trigger_id[-1])
        # Save
        self.message_id.append(message_id)
        self.msg_hash.append(msg_hash)
        self.trigger_id.append(trigger_id)
        self.image_url.append(image_url)


def image_gen(msg, generator):
    res = llm_davinci(prompt_use_in_image+Prompt_template.format(prompt=msg))
    r = json.loads(res)
    purpose = r["purpose"]
    model = r["model"]
    if purpose == 'generate':
        generator.classify_prompt(msg)
        generator.generate_image(model)
        response = f"I have generated the image according to the prompt : {generator.prompt} for you"
        image_url = generator.get_image_url()
    elif purpose == 'modify':
        if model == 'stable diffusion':
            response = "Sorry, we don't support stable diffusion model for modification yet, but I can generate a new image of it, please type the new image you want me to generate."
            image_url = None
            return response, image_url
        else:
            index_num = llm_davinci(
                prompt_for_image_modified.format(prompt=msg))
            mode, index = index_num.split(',')
            if mode == 'new':
                generator.classify_prompt(msg)
                generator.generate_image(model)
                response = f"I have generated the image according to the prompt : {generator.prompt} for you"
                image_url = generator.get_image_url()
            else:
                generator.modify_image(mode, index)
                response = f"I have according to your instruction to modified the model, and here is the photos: "
                image_url = generator.get_image_url()
    return response, image_url


# logic flow:
# 1) empty->do classification(repeatly)
# 2) ask for model Use
# 3) return the image Url
# 4) making follow up, if it is needed
# updated: just let all the task done by LLM, unless the user request in the prompt


# updated logic flow
# when new user prompt come, just do the classification for prompt and the model use
# store it in the class
# if it is a new request -> do the classification and return the url link
# if ask for modification -> check the last one model is using mid-journey or not, if yes -> do the modification and return the url link, if not -> return the not support message/ or just create a new one
