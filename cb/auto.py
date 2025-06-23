# this is an attempt to code the autocomplete feature 

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from playwright.sync_api import sync_playwright
import time

# Set your Gemini API key here
GOOGLE_API_KEY = "AIzaSyAg_2eibUL8r7qODzAqTHYJVqhW3g23kCI"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# Use Playwright to open a browser and search Google
def search_google(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # show browser
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.fill("textarea[name='q']", query)
        page.keyboard.press("Enter")
        time.sleep(3)  # wait for results
        content = page.content()
        page_title = page.title()
        page_url = page.url
        browser.close()
        return content[:2000], page_title, page_url  # trim to 2k chars for Gemini

# Step 1: Search Google
html_snippet, title, url = search_google("last El Clasico score Real Madrid vs Barcelona")

# Step 2: Ask Gemini to summarize from the HTML
response = llm.invoke(
    f"""The following is the HTML of a Google search result page.
Summarize the score of the last El Clasico from this content:\n\n{html_snippet}
"""
)

# Step 3: Show result
print("🧠 Gemini Summary:")
print(response.content)
