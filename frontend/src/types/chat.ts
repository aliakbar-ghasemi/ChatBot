export interface Message {
  id: number
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
  model: string | null
}

export interface Model {
  name: string;
  displayName: string;
}