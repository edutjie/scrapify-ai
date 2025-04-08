from openai import AsyncOpenAI
from app.config.settings import get_settings
import instructor
from pydantic import BaseModel


class LLMService:
    def __init__(self):
        self.settings = get_settings()
        self.default_model = self.settings.openai_default_model

    async def generate_response(
        self,
        query: str,
        api_key: str,
        model: str = None,
        temperature: float = 0.7,
        response_model: BaseModel | str | int | float | bool = str,
    ) -> BaseModel | str | int | float | bool:
        """
        Generate a response from the LLM using OpenAI.

        Args:
            query: The user's query
            api_key: OpenAI API key from request header
            model: The OpenAI model to use (optional, defaults to settings)
            temperature: Sampling temperature (optional, defaults to 0.7)
            response_model: The pydantic model or primitive type to use for the response (optional, defaults to str)

        Returns:
            The LLM's response as a pydantic model instance or primitive type.
        """
        try:
            client = AsyncOpenAI(api_key=api_key)
            client = instructor.from_openai(client)
            model_to_use = model or self.default_model
            completion = await client.chat.completions.create(
                model=model_to_use,
                response_model=response_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query},
                ],
                temperature=temperature,
            )

            return completion
        except Exception as e:
            raise Exception(f"Error generating LLM response: {str(e)}")
