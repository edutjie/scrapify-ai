import json
import requests
from app.config.settings import get_settings
from app.services.llm_service import LLMService


class LinkedInScraperService:
    def __init__(self):
        self.proxycurl_api_endpoint = "https://nubela.co/proxycurl/api/linkedin/company"
        self.settings = get_settings()
        self.llm_service = LLMService()

    async def scrape_company(self, linkedin_url: str):
        """
        Scrape a company's LinkedIn page using Proxycurl API
        """
        headers = {"Authorization": f"Bearer {self.settings.proxycurl_api_key}"}
        params = {
            "url": linkedin_url,
            "categories": "include",
            "funding_data": "include",
            "exit_data": "include",
            "acquisitions": "include",
            "extra": "include",
            "use_cache": "if-present",
            "fallback_to_cache": "on-error",
        }

        response = requests.get(
            self.proxycurl_api_endpoint, params=params, headers=headers
        )

        if response.status_code != 200:
            raise Exception(f"Failed to scrape LinkedIn company: {response.text}")

        return json.loads(response.text)
