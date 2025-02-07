export interface Message {
  id: number
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
}

export interface Model {
  name: string;
  displayName: string;
}