import requests
import re
from urllib.parse import urlparse, urljoin
from modules.utils import write_output
import urllib3

# Disable SSL warnings to avoid unnecessary warnings for insecure connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def is_valid_url(url):
    """
    Validate if the URL has a scheme (e.g., http, https) and a network location (e.g., domain, IP address).
    
    :param url: The URL to validate.
    :return: True if the URL has both a scheme and network location, False otherwise.
    """
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

def parameter_finder(file, output, output_format):
    """
    Extracts parameters from URLs found in the provided file and formats them as {url}?param=FUZZ.
    
    :param file: Path to the file containing URLs with status and additional text.
    :param output: Output file to save the formatted parameters.
    :param output_format: Format (txt or json) for saving the output.
    """
    # Read lines from the file containing URLs
    with open(file, 'r') as f:
        lines = f.read().splitlines()

    all_params = set()  # Set to store unique parameters found
    url_param_map = {}  # Dictionary to map URLs to their parameters

    # Process each line to extract URLs and parameters
    for line in lines:
        # Extract the URL from the line, ignoring the status and any additional text
        match = re.search(r'\[\+\] Found: (.+?) \(Status:', line)
        if match:
            url = match.group(1)
            # Skip invalid URLs
            if not is_valid_url(url):
                print(f"Invalid URL: {url}")
                continue
            
            try:
                # Send a GET request to the URL
                response = requests.get(url, verify=False)
                # Find all href attributes in the HTML response
                found_urls = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
                for found_url in found_urls:
                    # Convert relative URLs to absolute URLs if necessary
                    if not is_valid_url(found_url):
                        found_url = urljoin(url, found_url)
                    # Extract parameters if the URL contains a query string
                    if '?' in found_url:
                        parts = found_url.split('?')
                        params = parts[1].split('&')
                        for param in params:
                            param_key = param.split('=')[0]
                            # Add the parameter to the set if it is not already present
                            if param_key not in all_params:
                                all_params.add(param_key)
                                if url not in url_param_map:
                                    url_param_map[url] = []
                                url_param_map[url].append(param_key)
                                print(f"Found parameter in {found_url}")
            except requests.RequestException as e:
                # Handle request exceptions
                print(f"Error accessing {url}: {str(e)}")

    # Format the results as {url}?param=FUZZ
    results = []
    for url, params in url_param_map.items():
        for param in params:
            results.append(f"{url}?{param}=FUZZ")

    # Print all formatted results
    for result in results:
        print(result)
    
    # Write the results to the output file if specified
    if output:
        write_output(output, results, output_format)
