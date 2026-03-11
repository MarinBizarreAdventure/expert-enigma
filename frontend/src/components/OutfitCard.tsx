import { Shirt } from "lucide-react";
import type { Outfit } from "../types";

export function OutfitCard({ outfit }: { outfit: Outfit }) {
  return (
    <div className="mt-3 rounded-xl border border-white/5 bg-surface-700 p-4">
      <div className="flex items-center gap-2 mb-3">
        <Shirt className="w-4 h-4 text-indigo-400" />
        <span className="text-sm font-semibold text-white">What to wear</span>
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        {outfit.items.map((item) => (
          <span
            key={item}
            className="px-2.5 py-1 rounded-full text-xs bg-indigo-500/15 text-indigo-300 border border-indigo-500/20"
          >
            {item}
          </span>
        ))}
      </div>

      <p className="text-xs text-gray-400 leading-relaxed">{outfit.reasoning}</p>
    </div>
  );
}
