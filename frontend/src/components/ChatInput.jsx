function ChatInput({
  message,
  setMessage,
  sendMessage,
  loading,
}) {
  return (
    <div
      style={{
        borderTop: "1px solid #ddd",
        padding: "20px",
        display: "flex",
        gap: "10px",
      }}
    >
      <input
        value={message}
        placeholder="Ask SecondMind anything..."
        onChange={(e) =>
          setMessage(e.target.value)
        }
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            sendMessage();
          }
        }}
        style={{
          flex: 1,
          padding: "12px",
          borderRadius: "8px",
          border: "1px solid #ccc",
        }}
      />

      <button
        onClick={sendMessage}
        disabled={loading}
      >
        Send
      </button>
    </div>
  );
}

export default ChatInput;