import { OPENAI_API_TYPE } from '../utils/app/const';

export interface OpenAIModel {
  id: string;
  name: string;
  maxLength: number; // maximum length of a message
  tokenLimit: number;
}

  
export enum OpenAIModelID {
  Azure_gpt35 = 'gpt35',
  Vicuna = 'Vicuna',
  Azure_gpt4 = 'gpt4',
  Chatbison = 'google-chatbison',
  }
// in case the `DEFAULT_MODEL` environment variable is not set or set to an unsupported model
export const fallbackModelID = OpenAIModelID.Azure_gpt35;

export const OpenAIModels: Record<OpenAIModelID, OpenAIModel> = {
  [OpenAIModelID.Azure_gpt35]: {
  id: OpenAIModelID.Azure_gpt35,
  name: 'Azure_gpt35',
  maxLength: 96000,
  tokenLimit: 32768,
  },
  [OpenAIModelID.Vicuna]: {
    id: OpenAIModelID.Vicuna,
    name: 'Vicuna',
    maxLength: 96000,
    tokenLimit: 32768,
    },
  [OpenAIModelID.Azure_gpt4]: {
  id: OpenAIModelID.Azure_gpt4,
  name: 'Azure_gpt4',
  maxLength: 96000,
  tokenLimit: 32768,
  },
  [OpenAIModelID.Chatbison]: {
    id: OpenAIModelID.Chatbison,
    name: 'Chatbison',
    maxLength: 96000,
    tokenLimit: 32768,
    },
  };