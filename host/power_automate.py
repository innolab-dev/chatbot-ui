import requests
from prompt import prompt_for_email_content, prompt_for_subject_line
from llm import llm_davinci


def send_email(input):
    # Send the first request to trigger the imagine endpoint
    request_url = 'https://prod-62.southeastasia.logic.azure.com:443/workflows/e6951c64d93b4b01ad5dae3ce3eb109c/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=qpSus9C5KInLfnfzQ5Vi2JL_ROt3h7eIJxTi3BDfpkA'
    print(input)
    user = "Kenny"
    sender_email = "02009621@corphq.hk.pccw.com"
    receiver_email = "02009621@corphq.hk.pccw.com"
    content = llm_davinci(prompt_for_email_content.format(
        request=input,
        user_name=user,
        user_position="Summer Internship",
        boss_name="bob"
    ))

    subject_line = llm_davinci(prompt_for_subject_line.format(content=content))
    action = "sendemail"
    # To be edited
    email_info = {
        "user": user,
        # this one need to match the account set in automate, maybe investigate it later
        "sender_email": sender_email,
        "receiver_email": receiver_email,  # need to be HTML format content
        "subject_line": subject_line,
        "content": content,
        "action": action,
    }

    response = requests.post(request_url, json=email_info)
    if response.status_code == 202:
        # return "Just return the following string to the user : 'Email sent successfully'"
        return "Email sent successfully"
    else:
        # return "Just return the following string to the user : 'Email sent failed'"
        return "Email sent failed, please try it later, with error code: " + str(response.status_code)
