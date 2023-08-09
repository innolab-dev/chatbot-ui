prompt_for_classfication = """
I want you to classify prompts into one of 3 categories:

1) Image-related 
- Any prompt that involves generating, modifying, or describing an image, pictures, photos

2) Code-related
- Any prompt that involves writing code or explaining code

3) Question-answering
- Any prompt that is asking a question that requires a factual answer 
- Or any casual talk
- if you think it is not Image-related or the code-related, just output this one

I will provide a prompt. Your response should be the number corresponding to the category that best fits the prompt. Only respond with '1', '2' or '3'. 

Do not provide any additional explanation or text besides the category number.

Here are some examples:

Prompt: How tall is the Eiffel Tower?
Response: 3

Prompt: Hello, how do you feel today?
Response: 3

Prompt: Can you write a function in Python to reverse a string?
Response: 2 

Prompt: Can you generate the code of bfs in python for me?
Response: 2

Prompt: Generate an image of a cat to me.
Response: 1

Prompt: Please make an image that combines the features of a dog and a cat.
Response: 1

Now classify this prompt: {prompt}
"""


prompt_for_image_description = """
Given a prompt for generating an image, extract a descriptive summary of the main elements that the image should contain. 

The description should be reasonably concise while capturing the key details. Do not include any explanatory text. Just return the description as a string.

Prompt: Generate an image of a cute puppy playing with a ball in a field of flowers on a sunny day. The puppy is fluffy and brown with floppy ears. 
Description: a fluffy brown puppy with floppy ears playing with a ball in a field of flowers on a sunny day

Prompt: Make an image of a blue and red parrot perched on a branch of a rainforest tree. The parrot has bright feathers and looks down curiously. Lush green leaves surround it.
Description: a blue and red parrot with bright feathers perched on a rainforest tree branch surrounded by green leaves

Prompt: {prompt}
Description:
"""


prompt_for_image_modified = """
I will provide a prompt describing a request to modify generated images. Please parse the prompt and return a string in the format 'mode,index' based on the following:

I have 4 image indexes - 1, 2, 3, 4 (top left, top right, bottom left, bottom right)

Modes:

new: Generate a new image on a completely different topic. Return 'new,1'.
upscale: Enlarge or upscale an existing image. Return 'upscale,index'.
variation: Make changes to an existing image. Return 'variation,index'.
reset: Regenerate the existing images with the same prompts. Return 'reset,1'.
Do not return anything else besides the mode and index.

Examples:

Prompt: Can you draw a cat instead of a dog?
Ans: new,1

Prompt: Please zoom in on the top right image.
Ans: upscale,2

Prompt: Can you make some changes to the bottom left image?
Ans: variation,3

Prompt: Let's redo these with the same prompts.
Ans: reset,1

Prompt: {prompt}
Ans:
"""

prompt_for_email_content = """
Please draft the following email body in HTML format, with appropriate HTML tags for structure and formatting, on behalf of the user.

User request:
{request}

User background:
name: {user_name}
position: {user_position}   
boss_name: {boss_name}

"""
prompt_for_subject_line = """

Please review the email content, and give back the suitable subject line, 

here is the email content:
{content}
"""
