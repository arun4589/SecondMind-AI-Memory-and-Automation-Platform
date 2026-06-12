import { useState, useRef, useEffect } from "react";

import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import ChatInput from "./components/ChatInput";
import MemoryPanel from "./components/MemoryPanel";

import {
  chatApi,
  memoryApi,
} from "./services/api";

function App() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] =
  useState("");
  const [memories, setMemories] = useState([]);

  const [conversations, setConversations] =
    useState(() => {
      const saved = localStorage.getItem(
        "secondmind_conversations"
      );

      if (saved) {
        return JSON.parse(saved);
      }

      return [
        {
          id: crypto.randomUUID(),
          title: "Chat 1",
          messages: [],
        },
      ];
    });

  const [activeConversationId,
    setActiveConversationId] =
    useState(() => {
      return (
        localStorage.getItem(
          "secondmind_active_chat"
        ) || null
      );
    });

  const bottomRef = useRef(null);

  const activeConversation =
    conversations.find(
      (conv) =>
        conv.id === activeConversationId
    );

  useEffect(() => {
    if (
      !activeConversationId &&
      conversations.length > 0
    ) {
      setActiveConversationId(
        conversations[0].id
      );
    }
  }, [
    activeConversationId,
    conversations,
  ]);

  useEffect(() => {
    localStorage.setItem(
      "secondmind_conversations",
      JSON.stringify(conversations)
    );
  }, [conversations]);

  useEffect(() => {
    if (activeConversationId) {
      localStorage.setItem(
        "secondmind_active_chat",
        activeConversationId
      );
    }
  }, [activeConversationId]);

  useEffect(() => {
    fetchMemories();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [activeConversation, loading]);

  const fetchMemories = async () => {
    try {
      const data = await memoryApi();

      setMemories(data.memories);
    } catch (error) {
      console.error(error);
    }
  };

  const updateConversationMessages = (
    conversationId,
    newMessages
  ) => {
    setConversations((prev) =>
      prev.map((conv) =>
        conv.id === conversationId
          ? {
              ...conv,
              messages: newMessages,
            }
          : conv
      )
    );
  };

  const sendMessage = async () => {
  if (
    !message.trim() ||
    !activeConversation
  )
    return;

  const currentMessage = message;

  if (
    activeConversation.messages.length === 0
  ) {
    setConversations((prev) =>
      prev.map((conv) =>
        conv.id === activeConversationId
          ? {
              ...conv,
              title:
                currentMessage.length > 25
                  ? currentMessage.slice(
                      0,
                      25
                    ) + "..."
                  : currentMessage,
            }
          : conv
      )
    );
  }

  const userMessage = {
    role: "user",
    content: currentMessage,
  };

  const updatedMessages = [
    ...activeConversation.messages,
    userMessage,
  ];

  updateConversationMessages(
    activeConversationId,
    updatedMessages
  );

  setMessage("");
  setLoading(true);
  setStreamingMessage("");

  try {

    const response = await fetch(
      "http://localhost:8000/chat/stream",
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/json",
        },
        body: JSON.stringify({
          message: currentMessage,
          thread_id:
            activeConversationId,
        }),
      }
    );

    const reader =
      response.body.getReader();

    const decoder =
      new TextDecoder();

    let finalMessage = "";

    while (true) {

      const {
        done,
        value,
      } = await reader.read();

      if (done) break;

      const chunk =
        decoder.decode(value);

      const lines =
        chunk.split("\n");

      for (const line of lines) {

        if (
          line.startsWith("data:")
        ) {

          try {

            const json =
              JSON.parse(
                line.replace(
                  "data:",
                  ""
                )
              );

            finalMessage +=
              json.token;

            setStreamingMessage(
              finalMessage
            );

          } catch (e) {
            console.error(e);
          }

        }

      }

    }

    const assistantMessage = {
      role: "assistant",
      content: finalMessage,
    };

    updateConversationMessages(
      activeConversationId,
      [
        ...updatedMessages,
        assistantMessage,
      ]
    );

    setStreamingMessage("");

  } catch (error) {

    console.error(error);

    updateConversationMessages(
      activeConversationId,
      [
        ...updatedMessages,
        {
          role: "assistant",
          content:
            "Unable to connect to SecondMind backend.",
        },
      ]
    );

  } finally {

    setLoading(false);

    await fetchMemories();

  }
};

  const createNewChat = () => {
    const newConversation = {
      id: crypto.randomUUID(),
      title: `Chat ${
        conversations.length + 1
      }`,
      messages: [],
    };

    setConversations((prev) => [
      ...prev,
      newConversation,
    ]);

    setActiveConversationId(
      newConversation.id
    );
  };

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        fontFamily: "Arial",
      }}
    >
      <Sidebar
        conversations={conversations}
        activeConversationId={
          activeConversationId
        }
        setActiveConversationId={
          setActiveConversationId
        }
        createNewChat={createNewChat}
      />

      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            padding: "20px",
            borderBottom:
              "1px solid #ddd",
          }}
        >
          <h2>
            SecondMind Assistant
          </h2>
        </div>

        <ChatArea
          activeConversation={
            activeConversation
          }
          loading={loading}
          streamingMessage={streamingMessage}
          bottomRef={bottomRef}
        />

        <ChatInput
          message={message}
          setMessage={setMessage}
          sendMessage={sendMessage}
          loading={loading}
        />
      </div>

      <MemoryPanel memories={memories} />
    </div>
  );
}

export default App;