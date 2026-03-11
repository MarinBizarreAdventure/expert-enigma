class ProfileNotFound(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"Profile not found for user: {user_id}")


class ProfileAlreadyExists(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"Profile already exists for user: {user_id}")


class WeatherUnavailable(Exception):
    def __init__(self, city: str):
        self.city = city
        super().__init__(f"Weather data unavailable for city: {city}")


class ScrapingFailed(Exception):
    def __init__(self, query: str):
        self.query = query
        super().__init__(f"Failed to scrape results for: {query}")


class AgentError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Agent error: {message}")


class ConversationNotFound(Exception):
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        super().__init__(f"Conversation not found: {conversation_id}")
