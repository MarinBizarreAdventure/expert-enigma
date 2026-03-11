import { useState } from "react";
import { MapPin, User, Sparkles } from "lucide-react";
import { createProfile } from "../api";
import type { Profile } from "../types";

interface Props {
  userId: string;
  onCreated: (profile: Profile) => void;
}

export function ProfileSetup({ userId, onCreated }: Props) {
  const [name, setName] = useState("");
  const [city, setCity] = useState("");
  const [style, setStyle] = useState("");
  const [budget, setBudget] = useState("medium");
  const [dietary, setDietary] = useState("");
  const [cuisines, setCuisines] = useState("");
  const [avoid, setAvoid] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const splitTags = (val: string) =>
    val.split(",").map((s) => s.trim()).filter(Boolean);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim() || !city.trim()) {
      setError("Name and city are required.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const profile = await createProfile({
        user_id: userId,
        name: name.trim(),
        default_city: city.trim(),
        style_preferences: splitTags(style),
        budget_default: budget,
        dietary_restrictions: splitTags(dietary),
        favorite_cuisines: splitTags(cuisines),
        avoid: splitTags(avoid),
      });
      onCreated(profile);
    } catch {
      setError("Failed to create profile. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-500/20 mb-4">
            <Sparkles className="w-8 h-8 text-indigo-400" />
          </div>
          <h1 className="text-2xl font-bold text-white">Expert Enigma</h1>
          <p className="text-gray-400 mt-1">Your personal going-out assistant</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-surface-800 border border-white/5 rounded-2xl p-6 space-y-4"
        >
          <h2 className="text-lg font-semibold text-white">Set up your profile</h2>

          <Field label="Your name *">
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Marin"
                className="input pl-9"
              />
            </div>
          </Field>

          <Field label="Default city *">
            <div className="relative">
              <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
              <input
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                placeholder="Chisinau"
                className="input pl-9"
              />
            </div>
          </Field>

          <Field label="Style preferences" hint="comma-separated, e.g. smart casual, streetwear">
            <input
              type="text"
              value={style}
              onChange={(e) => setStyle(e.target.value)}
              placeholder="smart casual, streetwear"
              className="input"
            />
          </Field>

          <Field label="Budget">
            <select value={budget} onChange={(e) => setBudget(e.target.value)} className="input">
              <option value="low">Low ($)</option>
              <option value="medium">Medium ($$)</option>
              <option value="medium-high">Medium-High ($$$)</option>
              <option value="high">High ($$$$)</option>
            </select>
          </Field>

          <Field label="Dietary restrictions" hint="comma-separated">
            <input
              type="text"
              value={dietary}
              onChange={(e) => setDietary(e.target.value)}
              placeholder="vegetarian, no seafood"
              className="input"
            />
          </Field>

          <Field label="Favorite cuisines" hint="comma-separated">
            <input
              type="text"
              value={cuisines}
              onChange={(e) => setCuisines(e.target.value)}
              placeholder="italian, local cuisine"
              className="input"
            />
          </Field>

          <Field label="Avoid" hint="places/vibes you don't like">
            <input
              type="text"
              value={avoid}
              onChange={(e) => setAvoid(e.target.value)}
              placeholder="loud clubs, karaoke bars"
              className="input"
            />
          </Field>

          {error && <p className="text-red-400 text-sm">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium transition-colors"
          >
            {loading ? "Creating profile…" : "Get started"}
          </button>
        </form>
      </div>
    </div>
  );
}

function Field({
  label,
  hint,
  children,
}: {
  label: string;
  hint?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-1">
      <label className="text-sm text-gray-300">
        {label}
        {hint && <span className="text-gray-500 ml-1 font-normal">— {hint}</span>}
      </label>
      {children}
    </div>
  );
}
