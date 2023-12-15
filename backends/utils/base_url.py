from urllib.parse import urlsplit


def get_base_url(url):
    parsed_url = urlsplit(url)

    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    return base_url
