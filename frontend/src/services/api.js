import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const postChat = (chat) => api.post("/api/chat", { chat });

export default api;
