import ChatMessage from "./ChatMessage";

function ChatArea({
  activeConversation,
  loading,
  streamingMessage,
  bottomRef,
}) {
  return (
    <div
      style={{
        flex: 1,
        overflowY: "auto",
        padding: "20px",
      }}
    >
      {activeConversation?.messages
        .length === 0 &&
        !streamingMessage && (
          <div
            style={{
              textAlign: "center",
              marginTop: "150px",
              color: "gray",
            }}
          >
            <h2>Welcome to SecondMind</h2>

            <p>
              Your AI Memory &
              Automation Platform
            </p>
          </div>
        )}

      {activeConversation?.messages.map(
        (msg, index) => (
          <ChatMessage
            key={index}
            role={msg.role}
            content={msg.content}
          />
        )
      )}

      {streamingMessage && (
        <ChatMessage
          role="assistant"
          content={streamingMessage}
        />
      )}

      {loading &&
        !streamingMessage && (
          <div>
            <strong>
              SecondMind:
            </strong>
            <p>Thinking...</p>
          </div>
        )}

      <div ref={bottomRef}></div>
    </div>
  );
}

export default ChatArea;