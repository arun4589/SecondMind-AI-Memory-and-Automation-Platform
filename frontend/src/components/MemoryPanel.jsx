function MemoryPanel({ memories }) {
  return (
    <div
      style={{
        width: "320px",
        borderLeft: "1px solid #ddd",
        padding: "20px",
        overflowY: "auto",
        backgroundColor: "#fafafa",
      }}
    >
      <h3>Memory</h3>

      {memories.length === 0 ? (
        <p>No memories yet.</p>
      ) : (
        memories.map((memory, index) => (
          <div
            key={index}
            style={{
              padding: "12px",
              marginBottom: "10px",
              backgroundColor: "#f0f0f0",
              borderRadius: "8px",
            }}
          >
            {memory}
          </div>
        ))
      )}
    </div>
  );
}

export default MemoryPanel;