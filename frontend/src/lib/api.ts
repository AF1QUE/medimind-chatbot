import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Update this with your backend URL

export interface ChatMessage {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
}

export const sendMessage = async (
  message: string,
  conversationId?: string
): Promise<ChatResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/chat`, {
      message,
      conversation_id: conversationId,
    });
    return response.data;
  } catch (error) {
    console.error("Error sending message:", error);
    throw error;
  }
};
