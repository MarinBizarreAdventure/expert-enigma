import type { Profile } from "./types";

const BASE = "http://localhost:8000/api/v1";

export async function getProfile(userId: string): Promise<Profile | null> {
  const res = await fetch(`${BASE}/profile/${userId}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createProfile(data: Omit<Profile, "user_id"> & { user_id: string }): Promise<Profile> {
  const res = await fetch(`${BASE}/profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function sendMessage(params: {
  user_id: string;
  message: string;
  conversation_id: string | null;
}) {
  const res = await fetch(`${BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{
    conversation_id: string;
    reply: string;
    places?: import("./types").Place[];
    outfit?: import("./types").Outfit;
  }>;
}
