import json

def parse_headers(header_list):
    """
    Parse a list of headers into a dictionary.

    Args:
        header_list (list of str): List of headers in the format 'Key: Value'.

    Returns:
        dict: Dictionary of headers with keys and values stripped of leading/trailing whitespace.
    """
    headers = {}  # Initialize an empty dictionary to store headers
    for header in header_list:
        key, value = header.split(':')  # Split each header into key and value
        headers[key.strip()] = value.strip()  # Strip whitespace and add to the dictionary
    return headers  # Return the dictionary of parsed headers

def write_output(output, results, output_format):
    # Write output in the specified format (JSON or plain text)
    if output_format == 'json':
        # Write each URL on a new line in JSON format
        with open(output, 'w') as f:
            json.dump(results, f, indent=4)  # Using indent=4 for pretty JSON
    else:
        # Write each URL on a new line in plain text format
        with open(output, 'w') as f:
            for line in results:
                f.write(line + '\n')