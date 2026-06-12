function ChatMessage({ role, content }) {
  const isUser = role === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: "12px"
      }}
    >
      <div
        style={{
          maxWidth: "70%",
          padding: "12px",
          borderRadius: "12px",
          backgroundColor: isUser
            ? "#2563eb"
            : "#e5e7eb",
          color: isUser
            ? "white"
            : "black"
        }}
      >
        {content}
      </div>
    </div>
  );
}

export default ChatMessage;