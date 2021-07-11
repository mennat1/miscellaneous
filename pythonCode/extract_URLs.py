# The program should, given a list of HTTP and HTTPS URLs as arguments, retrieve each URL as a document
# and return the number of UNIQUE external URLs referenced in the document.
# Your program must parse HTML document responses, although you may optionally choose to also parse other
# document types for external URLs.  
# For example, an invocation with a list of URLs should look something like:
# "program http://example.com http://www.columbia.edu/~fdc/sample.html". 
# For each VALID URL, your program should print a line consisting of the URL and the number of external links
# in the retrieved document, separated by a space, like "http://example.com 1". 
# Each URL should be printed on its own line of the output. In a comment at the top of your main program file.

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    This will make sure that a proper scheme (protocol, e.g http or https) and domain name exists in the URL.
    """
    # print(f"Validating {url}")
    parsed = urlparse(url)
    validity = bool(parsed.netloc) and bool(parsed.scheme)
    # print(f"validity = {validity}")
    return validity


def extract_URLs(url):
    """
    Returns the number of UNIQUE external URLs referenced in the document "url"
    """
    # all URLs of `url`
    # print(f"Crawling URL: {url}")
    external_urls = set()
    # domain name of the URL without the protocol
    # We're gonna need the domain name to check whether the link we grabbed is external or internal.
    url_domain_name = urlparse(url).netloc
    # print(f"url_domain_name = {url_domain_name}")
    # Download the HTML content of the web page and wrap it with a soup object to ease HTML parsing.
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        # print(f"href = {href}")
        if href == "" or href is None:
            # href empty tag
            continue
        if is_valid(href):
            # print(f"Valid href = {href}")
            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc
            href_domain_name = parsed_href.netloc
            # print(f"valid href_domain_name = {href_domain_name}")
            if (href_domain_name != url_domain_name) and (href not in external_urls):
                # print(f"Found unique external URL = {href}")
                external_urls.add(href)

    print(f"{url} -> {len(external_urls)}")
    # print(f"external_urls = {external_urls}")
    return

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="A tool that extracts unique external URLs for each given valid URL document")
    parser.add_argument("url", help="The list of URLs to be crawled.")    
    args = parser.parse_args()
    url_list = args.url.split()
    for url in url_list:
        if is_valid(url):
            extract_URLs(url)
