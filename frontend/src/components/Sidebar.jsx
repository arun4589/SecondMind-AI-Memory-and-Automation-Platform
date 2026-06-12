function Sidebar({
  conversations,
  activeConversationId,
  setActiveConversationId,
  createNewChat,
}) {
  return (
    <div
      style={{
        width: "260px",
        borderRight: "1px solid #ddd",
        padding: "20px",
        backgroundColor: "#f8f9fa",
      }}
    >
      <h2>SecondMind</h2>

      <button
        onClick={createNewChat}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "20px",
        }}
      >
        + New Chat
      </button>

      <h4>Conversations</h4>

      {conversations.map((conv) => (
        <div
          key={conv.id}
          onClick={() =>
            setActiveConversationId(
              conv.id
            )
          }
          style={{
            padding: "10px",
            borderRadius: "8px",
            marginBottom: "10px",
            cursor: "pointer",
            backgroundColor:
              activeConversationId ===
              conv.id
                ? "#dbeafe"
                : "#e9ecef",
          }}
        >
          {conv.title}
        </div>
      ))}
    </div>
  );
}

export default Sidebar;