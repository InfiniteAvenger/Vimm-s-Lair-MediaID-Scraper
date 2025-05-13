import requests
from bs4 import BeautifulSoup
import json

# User agent to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Test extracting media ID from a specific game page
def test_media_id_extraction():
    url = "https://vimm.net/vault/2955"  # The URL you provided
    
    print(f"Testing media ID extraction from: {url}")
    
    response = requests.get(url, headers=HEADERS, verify=False)
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the title
    title_elem = soup.select_one('h2')
    title = title_elem.text.strip() if title_elem else "Title not found"
    print(f"Game title: {title}")
    
    # Find the media ID input
    media_id_input = soup.select_one('input[name="mediaId"]')
    
    if media_id_input:
        media_id = media_id_input['value']
        print(f"Media ID found: {media_id}")
    else:
        print("Media ID not found. Form structure may have changed.")
        
        # Look for any forms
        forms = soup.find_all('form')
        print(f"Found {len(forms)} forms on the page")
        
        # Check the first form's inputs
        if forms:
            inputs = forms[0].find_all('input')
            print(f"First form has {len(inputs)} inputs:")
            for i, input_tag in enumerate(inputs):
                print(f"  {i+1}. name={input_tag.get('name', 'None')}, type={input_tag.get('type', 'None')}")

# Run the test
test_media_id_extraction()
