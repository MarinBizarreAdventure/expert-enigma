import { useState, useEffect } from "react";
import { ProfileSetup } from "./components/ProfileSetup";
import { ChatPage } from "./components/ChatPage";
import { getProfile } from "./api";
import type { Profile } from "./types";

function getOrCreateUserId(): string {
  let id = localStorage.getItem("ee_user_id");
  if (!id) {
    id = `user-${Math.random().toString(36).slice(2, 10)}`;
    localStorage.setItem("ee_user_id", id);
  }
  return id;
}

export default function App() {
  const [userId] = useState(getOrCreateUserId);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    getProfile(userId)
      .then(setProfile)
      .catch(() => setProfile(null))
      .finally(() => setChecking(false));
  }, [userId]);

  function handleSignOut() {
    localStorage.removeItem("ee_user_id");
    window.location.reload();
  }

  if (checking) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-6 h-6 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  if (!profile) {
    return <ProfileSetup userId={userId} onCreated={setProfile} />;
  }

  return <ChatPage profile={profile} onSignOut={handleSignOut} />;
}
