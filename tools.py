from langchain.tools import tool
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
from rich import print
import requests 
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str :
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets"""
    results = tavily.search(query=query , max_results=1)

    out = []
    for r in results['results'] :
        out.append(
            f'Title : {r['title']}\n URL : {r['url']}\n Snippet : {r['content'][:200]}'
        )

        return "\n-----\n".join(out)

    
@tool
def scrape_url (url : str) -> str :
    """Scrape and return clean text content from a given URL for deeper reading"""
    try :
        resp = requests.get(url , timeout=20 , headers={"User_Agent" : "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text , "html.parser")
        for tag in soup(['script' , "style" , "nav" , "footer"]):
            tag.decompose()

            return soup.get_text(separator=" " , strip=True)[:500]
    except Exception as e :
        return f"Could not scape url : {str(e)}"