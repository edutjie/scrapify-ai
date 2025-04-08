from openai import AsyncOpenAI
from app.config.settings import get_settings


class LLMService:
    def __init__(self):
        self.settings = get_settings()
        self.default_model = self.settings.openai_default_model

    async def generate_response(
        self, query: str, api_key: str, model: str = None
    ) -> str:
        """
        Generate a response from the LLM using OpenAI.

        Args:
            query: The user's query
            api_key: OpenAI API key from request header
            model: The OpenAI model to use (optional, defaults to settings)

        Returns:
            The LLM's response as a string
        """
        try:
            client = AsyncOpenAI(api_key=api_key)
            model_to_use = model or self.default_model
            completion = await client.chat.completions.create(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query},
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
            )

            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating LLM response: {str(e)}")
