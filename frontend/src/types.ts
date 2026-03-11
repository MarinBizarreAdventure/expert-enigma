export interface Place {
  name: string;
  type: string;
  address: string;
  why: string;
  price_range?: string;
  url?: string;
  image_url?: string;
}

export interface Outfit {
  items: string[];
  reasoning: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  places?: Place[];
  outfit?: Outfit;
  timestamp: Date;
}

export interface Profile {
  user_id: string;
  name: string;
  default_city: string;
  style_preferences: string[];
  budget_default: string;
  dietary_restrictions: string[];
  favorite_cuisines: string[];
  avoid: string[];
}
