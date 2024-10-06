import streamlit as st
import requests
import random
from bs4 import BeautifulSoup
import urllib.parse

# Function to get autocomplete suggestions from DuckDuckGo
def get_autocomplete_suggestions(query):
    url = 'https://duckduckgo.com/ac/'
    params = {'q': query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        suggestions = [item['phrase'] for item in response.json()]
        return suggestions
    else:
        return []

# Function to perform search on DuckDuckGo and get result URLs
def get_search_results(query):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    params = {'q': query}
    response = requests.get('https://html.duckduckgo.com/html/', params=params, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_='result__a', href=True)
        urls = [link['href'] for link in links]
        return urls
    else:
        return []

def main():
    st.title("Random DuckDuckGo Search Result")
    initial_query = st.text_input("Enter your initial search query:", "")

    if st.button("Get Random Result"):
        if initial_query.strip() == "":
            st.error("Please enter a valid search query.")
            return

        with st.spinner("Fetching autocomplete suggestions..."):
            suggestions = get_autocomplete_suggestions(initial_query)
        
        if not suggestions:
            st.error("No autocomplete suggestions found.")
            return

        random_suggestion = random.choice(suggestions)
        st.write(f"Random Autocomplete Suggestion: **{random_suggestion}**")

        with st.spinner("Performing search..."):
            search_results = get_search_results(random_suggestion)
        
        if not search_results:
            st.error("No search results found.")
            return

        random_url = random.choice(search_results)
        st.success(f"Random Search Result URL: {random_url}")

        st.markdown(f"[Visit the URL]({random_url})")

if __name__ == "__main__":
    main()
