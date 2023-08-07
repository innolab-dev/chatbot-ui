import { OpenAIModel } from './openai';
import { ConversationBufferMemory} from 'langchain';


export interface Message {
  role: Role;
  content: string;
  image?: string; // Optional image property represented as a URL string
  // image?: File; // Optional image property represented as a file object
}

export type Role = 'assistant' | 'user';

export interface ChatBody {
  model: OpenAIModel;
  messages: Message[];
  key: string;
  prompt: string;
  temperature: number;
  //image
}

export interface Conversation {
  id: string;
  name: string;
  messages: Message[];
  model: OpenAIModel;
  prompt: string;
  temperature: number;
  folderId: string | null;
  memory:ConversationBufferMemory
}
