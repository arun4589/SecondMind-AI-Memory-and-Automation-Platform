import { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    try {
      const res = await axios.post(
        "http://localhost:8000/chat/",
        {
          message: message,
        }
      );

      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
      setResponse("Error connecting to backend");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>SecondMind</h1>

      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask something..."
        style={{
          width: "400px",
          padding: "10px",
        }}
      />

      <button
        onClick={sendMessage}
        style={{
          marginLeft: "10px",
          padding: "10px",
        }}
      >
        Send
      </button>

      <hr />

      <h3>Response</h3>

      <p>{response}</p>
    </div>
  );
}

export default App;
