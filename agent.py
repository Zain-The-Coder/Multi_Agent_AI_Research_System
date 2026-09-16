from langchain.agents import create_agent
from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url
from rich import print
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct" ,
    task="conversational",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=0.4,
)

model = ChatHuggingFace(llm=llm)

tools = {
    "web_search": web_search,
    "scrape_url": scrape_url
}

def search_agent () :
    return create_agent(
        model = model ,
        tools = [web_search]
    )

def reader_agent () :
    return create_agent(
        model = model ,
        tools = [scrape_url]
    )

writer_prompt = ChatPromptTemplate.from_messages([
    ("system" , "You are an expert research writer . Write clear , structured and insightful report") ,
    ("human" , '''Write a detailed search report on the topic below
Topic : {topic}
Research Gathered:
{research}

Structure the report as :
- Introduction
- Key finding (minimum well explained 3 points)
- Conslusion
- Sources (List all URLs found in the research)
Be detailed , factual and professional''')
])

writer_chain = writer_prompt | model | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system" , "You are a sharp anf constructive research critic . Be honest and sepcific") ,
    ("human" , '''Review the research report below and evaluate it strictly
Report : 
{report}

Respond in the exact format

Score : X/10

Strenghts :
- ...
- ...

Areas to improve :
- ...
- ...

One line verdict :
...''')
])

critic_chain = critic_prompt | model | StrOutputParser()