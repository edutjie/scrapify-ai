import requests
import json
from typing import Dict, Any


def search_google(query: str, api_key: str = None) -> Dict[str, Any]:
    """
    Search Google using the Serper API

    Args:
        query: The search query
        api_key: Serper API key (optional)

    Returns:
        Search results as a dictionary
    """
    url = "https://google.serper.dev/search"

    payload = json.dumps({"q": query})

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


def scrape_website(url: str, api_key: str = None) -> str:
    """
    Scrape a website using the Serper API and return the content as markdown

    Args:
        url: The URL to scrape
        api_key: Serper API key (optional)

    Returns:
        Website content as markdown string
    """
    api_url = "https://scrape.serper.dev"

    payload = json.dumps({"url": url, "includeMarkdown": True})

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    response = requests.request("POST", api_url, headers=headers, data=payload)
    try:
        data = json.loads(response.text)
        return data["markdown"]
    except Exception:
        return response.text
