"use client";

import { useState, useEffect, useRef } from "react";


type SourceItem = {
  content: string;
  source?: string;
  page?: number | null;
  chunk_id?: number | null;
};

type ChatMessage = {
  id?: number;
  role: "user" | "assistant";
  content: string;
  sources?: SourceItem[];
  isTyping?: boolean;
};

export default function Home() {
  const [mode, setMode] = useState<"chat" | "file">("chat");
  const [message, setMessage] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement | null>(null);
  const [openSources, setOpenSources] = useState<Record<number, boolean>>({});

  const API_URL = process.env.NEXT_PUBLIC_API_URL!;

  const typeText = async (fullText: string, sources?: SourceItem[]) => {
    const tempId = Date.now();

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "",
        sources,
        isTyping: true,
        id: tempId,
      } as ChatMessage & { id: number },
    ]);

    for (let i = 0; i < fullText.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 10));

      setMessages((prev) =>
        prev.map((msg) =>
          (msg as ChatMessage & { id?: number }).id === tempId
            ? { ...msg, content: fullText.slice(0, i + 1) }
            : msg
        )
      );
    }

    setMessages((prev) =>
      prev.map((msg) =>
        (msg as ChatMessage & { id?: number }).id === tempId
          ? { ...msg, isTyping: false }
          : msg
      )
    );
  };

  const handleSend = async () => {
    if (loading) return;
    if (!message.trim()) return;

    const userMessage = message;
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setMessage("");
    setLoading(true);

    try {
      if (mode === "chat") {
        const res = await fetch(`${API_URL}/chat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: userMessage }),
        });

        const data = await res.json();

        await typeText(data.reply || "No response received.");

      } else {
        if (!file) {
          alert("Please upload a file first");
          setLoading(false);
          return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("question", userMessage);

        const res = await fetch(`${API_URL}/ask-file`, {
          method: "POST",
          body: formData,
        });

        const data = await res.json();

        await typeText(
          data.answer || "No answer received.",
          data.sources || []
        );

      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Error occurred.",
        },
      ]);
    }

    setLoading(false);
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="min-h-screen bg-zinc-100 flex items-center justify-center p-6">
      <div className="w-full max-w-3xl bg-white border border-gray-200 rounded-2xl shadow-lg p-6 space-y-6">
        <h1 className="text-2xl font-bold text-center text-black">
          RAG AI Assistant
        </h1>

        {/* Mode Selector */}
        <div className="flex gap-2 justify-center">
          <button
            onClick={() => setMode("chat")}
            className={`px-4 py-2 rounded-lg transition ${mode === "chat"
              ? "bg-black text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
          >
            General Chat
          </button>

          <button
            onClick={() => setMode("file")}
            className={`px-4 py-2 rounded-lg transition ${mode === "file"
              ? "bg-black text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
          >
            File Chat
          </button>
        </div>

        {/* File Upload */}
        {mode === "file" && (
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Upload a PDF or DOCX file
            </label>

            <input
              type="file"
              accept=".pdf,.docx"
              disabled={loading}
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 file:mr-4 file:rounded-md file:border-0 file:bg-black file:px-4 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-gray-800 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />

            {file && (
              <p className="text-xs text-gray-500">
                Selected file: <span className="font-medium text-gray-700">{file.name}</span>
              </p>
            )}
          </div>
        )}

        {/* Chat History */}
        <div className="h-[420px] overflow-y-auto rounded-xl border border-gray-200 bg-zinc-50 p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center text-sm text-gray-500 text-center">
              Start a conversation in General Chat or upload a file in File Chat.
            </div>
          ) : (
            messages.map((msg, i) => (
              <div
                key={msg.id ?? i}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
              >
                <div className="max-w-[70%] md:max-w-[60%] space-y-2">
                  <div
                    className={`rounded-2xl px-4 py-3 text-sm whitespace-pre-wrap ${msg.role === "user"
                      ? "bg-black text-white"
                      : "bg-white border border-gray-200 text-black"
                      }`}
                  >
                    <>
                      {msg.content}
                      {msg.isTyping && <span className="animate-pulse">|</span>}
                    </>
                  </div>

                  {msg.role === "assistant" &&
                    msg.sources &&
                    msg.sources.length > 0 &&
                    !msg.content.includes("not explicitly available") && (
                      <div className="space-y-2">
                        <button
                          type="button"
                          onClick={() =>
                            setOpenSources((prev) => ({
                              ...prev,
                              [(msg.id ?? i)]: !prev[msg.id ?? i],
                            }))
                          }
                          className="text-xs font-semibold text-gray-500 px-1 hover:text-black transition"
                        >
                          {openSources[msg.id ?? i] ? "Hide Sources" : "Show Sources"}
                        </button>

                        {openSources[msg.id ?? i] && (
                          <div className="space-y-2">
                            {msg.sources.map((src, idx) => (
                              <div
                                key={idx}
                                className="rounded-lg border border-gray-200 bg-white p-3 text-xs text-black"
                              >
                                <div className="mb-1 text-gray-500">
                                  Page: {src.page ?? "-"}
                                </div>
                                <div>{src.content.slice(0, 200)}...</div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                </div>
              </div>
            ))
          )}

          {loading && !messages.some((msg) => msg.isTyping) && (
            <div className="flex justify-start">
              <div className="rounded-2xl px-4 py-3 text-sm bg-white border border-gray-200 text-gray-500">
                Thinking...
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Ask something..."
            value={message}
            disabled={loading}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !loading) {
                handleSend();
              }
            }}
            className="flex-1 border border-gray-300 bg-white px-4 py-3 rounded-lg text-black placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-black"
          />
          <button
            onClick={handleSend}
            disabled={loading || !message.trim()}
            className={`px-5 rounded-lg transition text-white ${loading || !message.trim()
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-black hover:bg-gray-800"
              }`}
          >
            {loading ? "Sending..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}