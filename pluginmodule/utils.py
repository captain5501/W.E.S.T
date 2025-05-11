import json
import pathlib

def save_results_as_txt(results, file_path):
    """
    Save the scan results to a text file with hyperlinks.
    
    Args:
        results (list): List of tuples containing file path, line number, and matched code.
        file_path (str): Path to the text file where results will be saved.
    """
    try:
        # Open the specified file for writing, with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as file:
            # Iterate through the results and write each one to the file
            for path, line_number, code in results:
                # Convert the file path to a URL format for use in hyperlinks
                url_path = f"file:///{pathlib.Path(path).as_posix().replace(':', '%3A')}"
                # Write the formatted result to the file
                file.write(f"Potential Vulnerability found on line {line_number} in file: {url_path}, Pattern matched: {code}\n")
        print(f"Results saved to {file_path}.")  # Notify the user of success
    except OSError as e:
        # Handle any OS-related errors during file operations
        print(f"Failed to save results to {file_path}: {e}")
    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")

def save_results_as_json(results, file_path):
    """
    Save the scan results to a JSON file with hyperlinks.
    
    Args:
        results (list): List of tuples containing file path, line number, and matched code.
        file_path (str): Path to the JSON file where results will be saved.
    """
    try:
        # Convert results into a list of dictionaries formatted for JSON
        results_json = [{
            'file': f"file:///{pathlib.Path(path).as_posix().replace(':', '%3A')}",
            'line': line_number,
            'code': code
        } for path, line_number, code in results]
        
        # Open the specified file for writing, with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write the JSON data to the file with indentation for readability
            json.dump(results_json, file, indent=4)
        print(f"Results saved to {file_path}.")  # Notify the user of success
    except OSError as e:
        # Handle any OS-related errors during file operations
        print(f"Failed to save results to {file_path}: {e}")
    except json.JSONDecodeError as e:
        # Handle errors related to JSON serialization
        print(f"Failed to serialize results to JSON: {e}")
    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")

def log_vulnerability(file_path, results):
    """
    Log detailed information about vulnerabilities to a log file with hyperlinks.
    
    Args:
        file_path (str): Path to the log file.
        results (list): List of tuples containing file path, line number, and matched code.
    """
    try:
        # Open the specified file for writing, with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as file:
            # Iterate through the results and write each one to the log file
            for path, line_number, code in results:
                # Convert the file path to a URL format for use in hyperlinks
                url_path = f"file:///{pathlib.Path(path).as_posix().replace(':', '%3A')}"
                # Write the formatted log entry to the file
                file.write(f"File: {url_path}, Line: {line_number}, Code: '{code}'\n")
        print(f"Vulnerabilities logged to {file_path}.")  # Notify the user of success
    except OSError as e:
        # Handle any OS-related errors during file operations
        print(f"Failed to log vulnerabilities to {file_path}: {e}")
    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")
