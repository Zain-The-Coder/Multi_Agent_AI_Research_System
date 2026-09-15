from langchain.tools import tool
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
import requests 
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str :
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets"""
    results = tavily.search(query="query" , max_results=2)

    out = []
    for r in results['results'] :
        out.append(
            f'Title : {r['title']}\n URL : {r['url']}\n Snippet : {r['content']}'
        )

    print(out)

