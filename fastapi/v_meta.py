import requests
from config import config

METADEFENDER_API_KEY = config["METADEFENDER_API_KEY"]

def metadefender(query_item, query_type):
    """Metadefender API for querying IP, domain, URL, or hash."""
    base_url = "https://api.metadefender.com/v4/"
    endpoint = ""

    if query_type == 'ip':
        endpoint = f"ip/{query_item}"
    elif query_type == 'domain':
        endpoint = f"domain/{query_item}"
    elif query_type == 'url':
        endpoint = "url"
    elif query_type == 'hash':
        endpoint = f"hash/{query_item}"
    else:
        raise ValueError("Invalid query_type. Must be 'ip', 'domain', 'url', or 'hash'.")

    url = f"{base_url}{endpoint}"
    headers = {
        'apikey': METADEFENDER_API_KEY
    }

    if query_type == 'url':
        # For URLs, Metadefender requires POST request with JSON data
        data = {"url": query_item}
        response = requests.post(url, headers=headers, json=data)
    else:
        response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {"error": f"Failed to retrieve data, status code: {response.status_code}"}
