import re
from pluginmodule.patterns import XSS_PATTERNS, SQLI_PATTERNS, SANITIZATION_PATTERNS, CUSTOM_PATTERNS

def contains_sanitization(line):
    """
    Check if a line contains any sanitization functions to avoid false positives.
    
    Args:
        line (str): The line of code to check.
        
    Returns:
        bool: True if sanitization functions are found, False otherwise.
    """
    return any(re.search(pattern, line) for pattern in SANITIZATION_PATTERNS)

def scan_file(file_path, patterns):
    """
    Scan a single PHP file for vulnerabilities using provided patterns.
    
    Args:
        file_path (str): The path to the PHP file.
        patterns (list): List of regex patterns to use for detecting vulnerabilities.
        
    Returns:
        list: A list of tuples containing file path, line number, and matched code.
    """
    results = []  # List to store results of detected vulnerabilities
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()  # Read all lines from the file
        for line_number, line in enumerate(lines, start=1):
            if not contains_sanitization(line):  # Check if the line is not sanitized
                for pattern in patterns:
                    match = re.search(pattern, line)  # Search for the pattern in the line
                    if match:
                        # Append the result with file path, line number, and matched code
                        results.append((file_path, line_number, match.group()))
    return results

def scan_files(file_paths, xss=False, sql=False, custom=False):
    """
    Scan multiple PHP files for vulnerabilities based on specified flags.
    
    Args:
        file_paths (list): List of file paths to scan.
        xss (bool): Flag to indicate scanning for XSS vulnerabilities.
        sql (bool): Flag to indicate scanning for SQL injection vulnerabilities.
        custom (bool): Flag to indicate scanning for Custom Patterns
        
    Returns:
        list: A list of tuples containing file path, line number, and matched code.
    """
    results = []  # List to store results of detected vulnerabilities
    patterns = []  # List to store patterns to use for detection
    
    # Add XSS patterns if xss flag is set
    if xss:
        patterns.extend(XSS_PATTERNS)
        
    # Add SQL injection patterns if sql flag is set
    if sql:
        patterns.extend(SQLI_PATTERNS)
    
    #Add Custom Patterns if custom flag is set
    if custom:
        patterns.extend(CUSTOM_PATTERNS)

    # Scan each file and collect results
    for file_path in file_paths:
        results.extend(scan_file(file_path, patterns))
    
    return results
