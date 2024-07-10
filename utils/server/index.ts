import { Message } from '@/types/chat';
import { OpenAIModel } from '@/types/openai';

import { AZURE_DEPLOYMENT_ID, OPENAI_API_HOST, OPENAI_API_TYPE, OPENAI_API_VERSION, OPENAI_ORGANIZATION } from '../app/const';

import {
  ParsedEvent,
  ReconnectInterval,
  createParser,
} from 'eventsource-parser';
import { log } from 'console';

export class OpenAIError extends Error {
  type: string;
  param: string;
  code: string;

  constructor(message: string, type: string, param: string, code: string) {
    super(message);
    this.name = 'OpenAIError';
    this.type = type;
    this.param = param;
    this.code = code;
  }
}
// Flask endpoint 
const FLASK_URL = 'http://localhost:5000/chat'




// connect to backend
export const OpenAIStream = async (
  userEmail: string,
  model: OpenAIModel,
  systemPrompt: string,
  temperature : number,
  conversationID: string,
  key: string,
  messages: Message[], 
  message: Message
) => {


  // Make request to Flask
  const res = await fetch(FLASK_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      userEmail,
      model,
      systemPrompt,
      temperature,
      conversationID,
      key,
      messages,
      message 
    })
  })
  const decoder = new TextDecoder();
  if (res.ok) {
    // Get Flask response
    const data = await res.json() 
    // Create stream from Flask response 
    const stream = new ReadableStream({
      async start(controller) {
        // Enqueue Flask text
        const text = data.text
        const image = data.image
        console.log("text", text)
        console.log(image)
        const encoder = new TextEncoder()

        const messageData = {
          text: text,
          image:image !== 'NULL' ? image : null
        }
        const queue = encoder.encode(JSON.stringify(messageData))
        // const queue = encoder.encode(text+'<img>'+image+'</img>')
        // const queue = encoder.encode(`${text}<img src="${image}" />`);

        controller.enqueue(queue)

        controller.close()
      }
    })
    
    return stream

  } else {
    throw new Error('Error fetching response from Flask')
  }

}





