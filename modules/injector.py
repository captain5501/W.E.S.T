import requests
import urllib3
from modules.utils import write_output

# Disable SSL warnings to avoid unnecessary warnings for insecure connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def inject_params(param_file, payload_file, output, output_format):
    """
    Injects payloads into parameters and checks for vulnerabilities.

    :param param_file: File containing URLs with FUZZ placeholder to test.
    :param payload_file: File containing payloads to inject into the URLs.
    :param output: Output file to save results.
    :param output_format: Output format (txt or json) for saving results.
    """
    
    # Read the parameterized URLs from the file
    with open(param_file, 'r') as file:
        param_list = file.read().splitlines()  # List of URLs with FUZZ placeholders

    # Read the payloads from the file
    with open(payload_file, 'r') as file:
        payloads = file.read().splitlines()  # List of payloads to inject
    
    results = []  # List to store the results

    # Define color codes for terminal output (green for non-vulnerable, red for vulnerable)
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    # Iterate over each URL template
    for param_url in param_list:
        for payload in payloads:
            # Replace FUZZ placeholder in the URL with the current payload
            test_url = param_url.replace('FUZZ', payload)
            try:
                # Send a GET request to the constructed URL
                response = requests.get(test_url, verify=False)
                # Check if the payload is reflected in the response
                if payload in response.text:
                    # If reflected, mark it as vulnerable
                    result = f"Vulnerable URL: {test_url} - Status: {response.status_code}"
                    colored_result = f"{RED}{result}{RESET}"  # Color output red for terminal
                else:
                    # If not reflected, mark it as non-vulnerable
                    result = f"Non-vulnerable URL: {test_url} - Status: {response.status_code}"
                    colored_result = f"{GREEN}{result}{RESET}"  # Color output green for terminal
                print(colored_result)  # Print the result with color
                results.append(result)  # Append uncolored result for saving to file
            except requests.RequestException as e:
                # Handle exceptions during request
                error = f"Error testing {test_url} ({str(e)})"
                print(error)  # Print the error message
                results.append(error)  # Append error to results list

    # Write the results to the specified output file
    if output:
        write_output(output, results, output_format)  # Call helper function to save results
