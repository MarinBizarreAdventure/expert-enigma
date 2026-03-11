import { useState, useRef, useEffect } from "react";
import { Send, LogOut, ChevronRight } from "lucide-react";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { sendMessage } from "../api";
import type { Message, Profile } from "../types";

interface Props {
  profile: Profile;
  onSignOut: () => void;
}

function genId() {
  return Math.random().toString(36).slice(2);
}

export function ChatPage({ profile, onSignOut }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: genId(),
      role: "assistant",
      text: `Hey ${profile.name}! 👋 I'm your going-out assistant. Tell me what you're planning — where, when, what kind of evening — and I'll find real places and suggest what to wear.`,
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [selectedPlace, setSelectedPlace] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function submit(text: string) {
    if (!text.trim() || loading) return;

    const userMsg: Message = {
      id: genId(),
      role: "user",
      text: text.trim(),
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    setSelectedPlace(null);

    try {
      const res = await sendMessage({
        user_id: profile.user_id,
        message: text.trim(),
        conversation_id: conversationId,
      });

      setConversationId(res.conversation_id);

      const assistantMsg: Message = {
        id: genId(),
        role: "assistant",
        text: res.reply,
        places: res.places,
        outfit: res.outfit,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errMsg: Message = {
        id: genId(),
        role: "assistant",
        text: "Something went wrong. Make sure the backend is running and try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit(input);
    }
  }

  function askAboutPlace(name: string) {
    submit(`Tell me more about ${name} — I'm considering going there.`);
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-surface-800/80 backdrop-blur shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center text-sm">✦</div>
          <div>
            <p className="font-semibold text-white text-sm">Expert Enigma</p>
            <p className="text-xs text-gray-500">{profile.default_city}</p>
          </div>
        </div>
        <button
          onClick={onSignOut}
          className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-gray-300 transition-colors"
        >
          <LogOut className="w-3.5 h-3.5" />
          Sign out
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-0">
        <div className="max-w-2xl mx-auto">
          {messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              message={msg}
              selectedPlace={selectedPlace}
              onSelectPlace={setSelectedPlace}
            />
          ))}
          {loading && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* Selected place action bar */}
      {selectedPlace && !loading && (
        <div className="px-4 py-2 bg-indigo-600/10 border-t border-indigo-500/20">
          <div className="max-w-2xl mx-auto flex items-center justify-between gap-3">
            <p className="text-sm text-indigo-300">
              <span className="text-indigo-400 font-medium">{selectedPlace}</span> selected
            </p>
            <button
              onClick={() => askAboutPlace(selectedPlace)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium transition-colors"
            >
              Ask for more details
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Input */}
      <div className="px-4 py-4 border-t border-white/5 bg-surface-800/80 backdrop-blur shrink-0">
        <div className="max-w-2xl mx-auto flex items-end gap-3">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Tell me what you're planning this evening…"
            rows={1}
            disabled={loading}
            className="flex-1 resize-none bg-surface-700 border border-white/10 rounded-xl px-4 py-3 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 disabled:opacity-50 transition-all max-h-32 overflow-y-auto"
            style={{ height: "auto" }}
            onInput={(e) => {
              const el = e.target as HTMLTextAreaElement;
              el.style.height = "auto";
              el.style.height = Math.min(el.scrollHeight, 128) + "px";
            }}
          />
          <button
            onClick={() => submit(input)}
            disabled={!input.trim() || loading}
            className="w-10 h-10 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center transition-colors shrink-0"
          >
            <Send className="w-4 h-4 text-white" />
          </button>
        </div>
        <p className="max-w-2xl mx-auto mt-2 text-xs text-gray-600 text-center">
          Enter to send · Shift+Enter for new line
        </p>
      </div>
    </div>
  );
}
