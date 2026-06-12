import axios from "axios";

const API_BASE = "http://localhost:8000";

export const chatApi = async (
  message,
  threadId
) => {
  const res = await axios.post(
    `${API_BASE}/chat/`,
    {
      message,
      thread_id: threadId,
    }
  );

  return res.data;
};

export const memoryApi = async () => {
  const res = await axios.get(
    `${API_BASE}/memory/7`
  );

  return res.data;
};