from typing import Dict, Any
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from app.tools.search_tools import search_google, scrape_website
from app.config.settings import get_settings


class AgentService:
    def __init__(self):
        self.agent = None
        self.settings = get_settings()

    def create_websearch_agent(
        self,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0,
        search_instructions: str = None,
    ) -> Any:
        """Create a ReAct agent with search and scraping tools"""

        # Define the tools
        @tool
        def google_search(query: str) -> Dict[str, Any]:
            """Search Google for information about a topic."""
            return search_google(query, self.settings.serper_api_key)

        @tool
        def website_scraper(url: str) -> str:
            """Scrape content from a website URL and return as markdown."""
            return scrape_website(url, self.settings.serper_api_key)

        llm = ChatOpenAI(api_key=api_key, model=model, temperature=temperature)
        tools = [google_search, website_scraper]
        system_prompt = f"""You are a helpful research assistant.
        Your goal is to provide accurate, detailed information to the user's questions.
        
        First, search Google to find relevant information about the user's query.
        If the Google search results don't provide enough information, scrape specific websites 
        mentioned in the search results to get more detailed information.
        
        You may need to perform multiple searches and scrapes to gather sufficient information.
        Always analyze the information you get critically and provide a coherent, comprehensive answer.
        
        Remember to cite your sources in your final answer.{"\n\nAdditional Instruction:\n" + search_instructions if search_instructions else ""}"""

        self.agent = create_react_agent(llm, tools, prompt=system_prompt)
        return self.agent

    def create_scrape_agent(
        self,
        api_key: str,
        web_url: str,
        model: str = "gpt-4o",
        temperature: float = 0,
        search_instructions: str = None,
    ) -> Any:
        """Create a ReAct agent focused on website scraping with ability to crawl links"""

        # Define the tools
        @tool
        def website_scraper(url: str) -> str:
            """Scrape content from a website URL and return as markdown."""
            return scrape_website(url, self.settings.serper_api_key)

        llm = ChatOpenAI(api_key=api_key, model=model, temperature=temperature)
        tools = [website_scraper]
        system_prompt = f"""You are a specialized web scraping assistant.
        Your goal is to extract and analyze information from websites to answer the user's questions.
        
        You will start by scraping the initial URL: {web_url}
        
        After scraping a page, look for relevant links within the content that might contain additional 
        information needed to answer the query. You can follow these links by scraping them as well.
        
        Follow these guidelines:
        1. First scrape the initial URL provided
        2. Analyze the content to find relevant information
        3. Identify links to other pages within the same domain that might contain more relevant information
        4. Scrape those additional pages when necessary
        5. Continue until you have gathered sufficient information to answer the query
        6. Prioritize depth over breadth - focus on the most promising paths
        
        Always provide a comprehensive answer based on the scraped content and cite the specific URLs 
        you used to gather information.{"\n\nAdditional Instruction:\n" + search_instructions if search_instructions else ""}"""

        self.agent = create_react_agent(llm, tools, prompt=system_prompt)
        return self.agent

    async def run_websearch_agent(
        self,
        query: str,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.5,
        search_instructions: str = None,
    ) -> str:
        """Run the agent with a user query"""
        agent = self.create_websearch_agent(
            api_key, model, temperature, search_instructions
        )
        print(f"Running agent with query: {query}")
        response = await agent.ainvoke({"messages": [("user", query)]})
        for message in response["messages"]:
            print(message)
        return response["messages"][-1].content

    async def run_scrape_agent(
        self,
        web_url: str,
        query: str,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.5,
        search_instructions: str = None,
    ) -> str:
        """Run the scraping agent with a user query and starting web URL"""
        agent = self.create_scrape_agent(
            api_key, web_url, model, temperature, search_instructions
        )
        print(f"Running scrape agent with query: {query} on website: {web_url}")
        response = await agent.ainvoke({"messages": [("user", query)]})
        for message in response["messages"]:
            print(message)
        return response["messages"][-1].content
