from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.utilities.google_search import GoogleSearchAPIWrapper
from llama_index.readers import BeautifulSoupWebReader
from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import urljoin

llm = ChatOpenAI(model="gpt-4-0613")

google_search = GoogleSearchAPIWrapper()

def link_results(query):
    return google_search.results(query,10)

def scraping(query):
    documents = BeautifulSoupWebReader().load_data(urls=[query])
    for i, document in enumerate(documents):
        text = re.sub(r'\n+', '\n', document.text)
        documents[i] = text[:1500]
    return documents

def scrape_links_and_text(url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all('a')  # find all a tags

    result = ""
    for link in links:
        # Use urljoin to ensure the link URL is absolute
        link_url = urljoin(url, link.get('href', ''))
        text = link.text.strip()  # strip removes leading/trailing whitespace
        result += f"{link_url} : {text}\n"  # Append the url and text to the result string

    return result[:1500]  # Truncate the result string to 1500 characters

tools = [
    Tool(
        name = "Search",
        func= link_results,
        description="useful for when you need to answer questions about current events. it is single-input tool Search."
    ),
    Tool(
        name = "Links",
        func= scrape_links_and_text,
        description="It is a convenient tool that allows you to obtain a list of URLs and texts by specifying a URL."
    ),
    Tool(
        name = "Scraping",
        func= scraping,
        description="It is a useful tool that can acquire content by giving a URL."
    ),
]

mrkl = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

def langchain_agent(question):
    try:
        result = mrkl.run(question)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        # 何らかのデフォルト値やエラーメッセージを返す
        return "An error occurred while processing the question"
 
