import anthropic

from app.core.config import settings


class ClaudeService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-sonnet-4-6"

    async def get_coaching_advice(self, user_data: dict, expert_result: dict) -> str:
        prompt = self._build_prompt(user_data, expert_result)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def _build_prompt(self, user_data: dict, expert_result: dict) -> str:
        return (
            f"You are PhysiqAI, an expert fitness coach.\n\n"
            f"User profile: {user_data}\n"
            f"Expert system analysis: {expert_result}\n\n"
            f"Provide a personalized workout and nutrition recommendation."
        )
