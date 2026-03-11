import { MapPin, ExternalLink, DollarSign } from "lucide-react";
import type { Place } from "../types";

interface Props {
  place: Place;
  selected: boolean;
  onSelect: () => void;
}

const FALLBACK = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&q=60";

export function PlaceCard({ place, selected, onSelect }: Props) {
  return (
    <div
      onClick={onSelect}
      className={`
        flex-shrink-0 w-64 rounded-xl overflow-hidden cursor-pointer transition-all duration-200
        border bg-surface-700
        ${selected
          ? "border-indigo-500 ring-2 ring-indigo-500/40 shadow-lg shadow-indigo-500/10"
          : "border-white/5 hover:border-white/15"
        }
      `}
    >
      <div className="h-36 overflow-hidden bg-surface-600">
        <img
          src={place.image_url || FALLBACK}
          alt={place.name}
          className="w-full h-full object-cover"
          onError={(e) => {
            (e.target as HTMLImageElement).src = FALLBACK;
          }}
        />
      </div>

      <div className="p-3 space-y-2">
        <div className="flex items-start justify-between gap-2">
          <div>
            <p className="font-semibold text-white text-sm leading-tight">{place.name}</p>
            <span className="text-xs text-indigo-400 capitalize">{place.type}</span>
          </div>
          {place.price_range && (
            <span className="flex items-center gap-0.5 text-xs text-gray-400 shrink-0">
              <DollarSign className="w-3 h-3" />
              {place.price_range}
            </span>
          )}
        </div>

        <div className="flex items-start gap-1.5 text-xs text-gray-400">
          <MapPin className="w-3 h-3 mt-0.5 shrink-0 text-gray-500" />
          <span className="line-clamp-1">{place.address}</span>
        </div>

        <p className="text-xs text-gray-300 line-clamp-2 leading-relaxed">{place.why}</p>

        {place.url && (
          <a
            href={place.url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="inline-flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 transition-colors mt-1"
          >
            <ExternalLink className="w-3 h-3" />
            Visit site
          </a>
        )}
      </div>
    </div>
  );
}
