from urllib.parse import urlsplit

def get_base_url(url):
    # Parse the URL using urlsplit
    parsed_url = urlsplit(url)
    
    # Construct the base URL using the scheme, netloc, and path
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    return base_url