import ReactMarkdown from "react-markdown";
import { PlaceCard } from "./PlaceCard";
import { OutfitCard } from "./OutfitCard";
import type { Message } from "../types";

interface Props {
  message: Message;
  selectedPlace: string | null;
  onSelectPlace: (name: string) => void;
}

export function MessageBubble({ message, selectedPlace, onSelectPlace }: Props) {
  if (message.role === "user") {
    return (
      <div className="flex justify-end mb-4">
        <div className="max-w-[75%] px-4 py-2.5 rounded-2xl rounded-br-sm bg-indigo-600 text-white text-sm leading-relaxed">
          {message.text}
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-end gap-3 mb-4">
      <div className="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center text-sm shrink-0">
        ✦
      </div>
      <div className="flex-1 min-w-0">
        <div className="bg-surface-700 border border-white/5 rounded-2xl rounded-bl-sm px-4 py-3">
          <div className="prose prose-sm prose-invert max-w-none text-gray-200 text-sm leading-relaxed">
            <ReactMarkdown>{message.text}</ReactMarkdown>
          </div>
        </div>

        {message.places && message.places.length > 0 && (
          <div className="mt-3">
            <div className="flex gap-3 overflow-x-auto pb-2 scroll-smooth">
              {message.places.map((place) => (
                <PlaceCard
                  key={place.name}
                  place={place}
                  selected={selectedPlace === place.name}
                  onSelect={() => onSelectPlace(place.name)}
                />
              ))}
            </div>
          </div>
        )}

        {message.outfit && <OutfitCard outfit={message.outfit} />}
      </div>
    </div>
  );
}
