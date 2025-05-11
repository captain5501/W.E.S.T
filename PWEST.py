import argparse
import logging
import os
from pluginmodule.scanner import scan_files
from pluginmodule.utils import save_results_as_txt, save_results_as_json, log_vulnerability

# Set up logging to record errors to a file named 'error.log'
logging.basicConfig(filename='error.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def run_plugin_scan(path, xss=False, sql=False, custom=False, output=None, log=False):
    """
    Run the PHP vulnerability scan with the specified parameters.
    
    :param path: Path to the folder containing PHP files to scan.
    :param xss: Enable scanning for XSS vulnerabilities.
    :param sql: Enable scanning for SQL injection vulnerabilities.
    :param custom: Enable scanning for custom patterns.
    :param output: Output file path for results (txt or json).
    :param log: Whether to log vulnerabilities to a file.
    """
    
    # Check if the provided path is valid
    if not os.path.isdir(path):
        raise ValueError(f"The provided path '{path}' does not exist or is not a directory.")

    # Collect all PHP files from the specified directory
    file_paths = [os.path.join(root, file)
                for root, _, files in os.walk(path)
                for file in files if file.endswith('.php')]

    # Scan files based on the selected vulnerability types
    results = scan_files(file_paths, xss=xss, sql=sql, custom=custom)

    # Save results in the specified format
    if output:
        if output.endswith('.txt'):
            save_results_as_txt(results, output)
        elif output.endswith('.json'):
            save_results_as_json(results, output)
        else:
            raise ValueError("Unsupported file extension. Please use '.txt' or '.json'.")

    # Log results to a file if the log flag is set
    if log:
        log_vulnerability('vulnerabilities.log', results)
        print("Results have been logged to 'vulnerabilities.log'.")

    print(f"Scan completed. Results saved to {output if output else 'console'}.")

if __name__ == '__main__':
    import argparse

    # Function to parse command-line arguments
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Run PHP Vulnerability Scanner")
        parser.add_argument('path', type=str, help='Path to the folder containing PHP files to scan.')
        parser.add_argument('--xss', action='store_true', help='Enable scanning for XSS vulnerabilities.')
        parser.add_argument('--sql', action='store_true', help='Enable scanning for SQL injection vulnerabilities.')
        parser.add_argument('--custom', action='store_true', help='Scan the files for Custom Patterns')
        parser.add_argument('-o', '--output', type=str, help='Output file path for results (txt or json).')
        parser.add_argument('--log', action='store_true', help='Log vulnerabilities to vulnerabilities.log')
        return parser.parse_args()

    # Parse the command-line arguments and run the plugin scan with the provided options
    args = parse_arguments()
    run_plugin_scan(
        path=args.path,
        xss=args.xss,
        sql=args.sql,
        custom=args.custom,
        output=args.output,
        log=args.log
    )