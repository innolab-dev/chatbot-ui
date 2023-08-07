# image_generator.py
from prompt import prompt_for_image_description, prompt_for_image_modified
from midjourney_handler import gen_image, upscale, reset, variation
from llm import llm_davinci


class ImageGenerator:

    def __init__(self):  # in main funtion
        self.context = None
        self.image_url = []
        self.message_id = []
        self.msg_hash = []
        self.trigger_id = []
        self.prompt = ""

    def classify_prompt(self, prompt):  # first step
        # Classify prompt
        self.prompt = llm_davinci(prompt_for_image_description.format(
            prompt=prompt))  # try to use llm, but even worst
        # self.prompt = prompt
        self.context = "finish extract prompt"

    def generate_image(self, model):  # third step
        # Generate image based on context
        if model == "diffusion":
            # image = generate_diffuse(prompt)
            image_url = "url"
        elif model == "midjourney":
            # replace the code in automate.py should be fine
            print(self.prompt)
            message_id, msg_hash, trigger_id, image_url = gen_image(
                self.prompt)
        self.context = "img formed"
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


def image_gen(data, state, generator):
    msg = data["messages"][-1]["content"]
    image_url = None
    print("here is image", generator.context)
    response = f'error occurs, with context of:{generator.context}'
    if generator.context is None:
        generator.classify_prompt(msg)  # get prompt
        state = "image"
        response = "choose model, midjourney or diffusion model"
    elif generator.context == "finish extract prompt":
        # middle ask for the model selection
        #     generator.context = "Wait for model selection"  # get model
        #     state = "image"
        # elif generator.context == "Wait for model selection":
        #     # generator.prompt = msg
        #     # for testing here,
        # msg is model here
        msg = "midjourney"
        generator.generate_image(msg)  # gen image
        response = f"I have generated the image according to the prompt : {generator.prompt} for you"
        image_url = generator.get_image_url()  # get url
        state = None
    elif generator.context == "img formed":
        # check whether start a new task or just continue
        index_num = llm_davinci(prompt_for_image_modified.format(prompt=msg))
        mode, index = index_num.split(',')
        print("hello", mode, index)
        if mode == 'new':
            # for testing here,
            generator.classify_prompt(msg)  # get prompt
            state = "image"
            response = f"I have generated the image according to the prompt : {generator.prompt} for you"
        else:
            generator.modify_image(mode, index)  # gen image
            if mode == 'upscale':
                generator.context = None
            response = f"I have according to your instruction to modified the model, and here is the photos: "
            image_url = generator.get_image_url()  # get url

    # for testing
    # response = "Sample images"
    # image_url = "https://cdn.discordapp.com/attachments/1128529072960569346/1131486774535929907/InnovationLab_HKT_japanese_soliders_dea6836d-a94f-420d-ae80-aa66c7260e70.png"
    # state = None
    return response, image_url, state


# logic flow:
# 1) empty->do classification(repeatly)
# 2) ask for model Use
# 3) return the image Url
# 4) making follow up, if it is needed
