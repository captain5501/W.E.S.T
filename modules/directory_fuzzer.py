import requests
import threading
import time
from modules.utils import write_output
import urllib3

# Disable SSL warnings to avoid unnecessary warnings for insecure connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def directory_fuzzer(url, wordlist, threads, delay, status_code, headers, output, output_format, error_output="error.txt"):
    """
    Fuzzes directories on a given URL using a wordlist and multithreading.
    
    Parameters:
        url (str): The base URL to test.
        wordlist (str): Path to the file containing the list of directory paths to test.
        threads (int): Number of threads to use for concurrent requests.
        delay (int or None): Delay in seconds between batches of requests.
        status_code (int or None): HTTP status code to match for a successful response.
        headers (dict): HTTP headers to include in the request.
        output (str or None): File to write successful results.
        output_format (str): Format to use for writing the successful results.
        error_output (str): File to write error messages. Default is "error.txt".
    """
    
    # Read the wordlist file and split it into a list of paths
    with open(wordlist, 'r') as file:
        paths = file.read().splitlines()
    
    results = []  # List to store successful results
    errors = []   # List to store errors

    def fuzz(url, path, status_code, headers):
        """
        Sends a GET request to the target URL with the given path and checks the response.
        
        Parameters:
            url (str): The base URL to test.
            path (str): The directory path to append to the base URL.
            status_code (int or None): Expected status code for a successful response.
            headers (dict): HTTP headers to include in the request.
        """
        target_url = f"{url}/{path}"  # Construct the full URL with the directory path
        try:
            response = requests.get(target_url, headers=headers, verify=False)  # Send GET request
            # Check if the response status code matches the expected status code (or if no status code is specified)
            if status_code is None or response.status_code == status_code:
                result = f"[+] Found: {target_url} (Status: {response.status_code})"
                print(result)  # Print the successful result
                results.append(result)  # Add the result to the results list
        except requests.RequestException as e:
            # Capture and handle request exceptions
            error = f"[-] Error: {target_url} ({str(e)})"
            errors.append(error)  # Add the error to the errors list
    
    # Process the wordlist in chunks based on the number of threads
    for i in range(0, len(paths), threads):
        threads_list = []
        for path in paths[i:i + threads]:
            # Create and start a new thread for each path
            t = threading.Thread(target=fuzz, args=(url, path, status_code, headers))
            threads_list.append(t)
            t.start()
        
        # Wait for all threads in the current batch to finish
        for t in threads_list:
            t.join()
        
        # Introduce a delay after every 5 requests if specified
        if delay and (i // threads) % 5 == 0:
            print(f"[DEBUG] Sleeping for {delay} seconds...")
            time.sleep(delay)
    
    # Write the successful results to the specified output file
    if output:
        write_output(output, results, output_format)
    
    # Write the errors to the specified error output file
    if errors:
        write_output(error_output, errors, 'txt')
