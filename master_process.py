import argparse
import os
from modules.directory_fuzzer import directory_fuzzer
from modules.parameter_finder import parameter_finder
from modules.injector import inject_params
from modules.utils import parse_headers

def get_valid_file(prompt):
    """
    Prompt the user to input a file path until a valid file is provided.
    
    :param prompt: Prompt message for the user.
    :return: Valid file path.
    """
    while True:
        file_path = input(prompt).strip()
        if os.path.isfile(file_path):
            return file_path
        else:
            print(f"File not found: {file_path}. Please try again.")

def master_process(url, wordlist, threads, delay, status_code, headers, output_suffix, output_format, payload_file=None):
    """
    Orchestrates directory fuzzing, parameter finding, and payload injection.
    
    :param url: Target URL
    :param wordlist: Path to wordlist file
    :param threads: Number of threads for fuzzing
    :param delay: Delay in seconds every 5 requests
    :param status_code: Status code to check (optional)
    :param headers: Custom headers for requests
    :param output_suffix: Suffix for output files
    :param output_format: Format for output files
    :param payload_file: Path to payload file (optional)
    """
    # Generate output filenames based on the provided suffix for each step of the process
    dfuzz_output_file = f'dfuzz_{output_suffix}.txt'
    param_output_file = f'param_{output_suffix}.txt'

    # Step 1: Run directory fuzzing
    print(f"[INFO] Starting Directory Fuzzer with {threads} threads")
    directory_fuzzer(
        url=url,
        wordlist=wordlist,
        threads=threads,
        delay=delay,
        status_code=status_code,
        headers=headers,
        output=dfuzz_output_file,
        output_format=output_format
    )
    
    # Step 2: Run parameter finder using the output from directory fuzzing
    print(f"[INFO] Running Parameter Finder using {dfuzz_output_file}")
    parameter_finder(
        file=dfuzz_output_file,
        output=param_output_file,
        output_format=output_format
    )
    
    # Step 3: Ask for payload file if not provided
    if payload_file is None:
        payload_file = get_valid_file("Enter the path to the payload file: ")
    
    # Perform injection using parameters found
    print(f"[INFO] Starting Payload Injection using {param_output_file}")
    inject_params(
        param_file=param_output_file,
        payload_file=payload_file,
        output=f'injection_results_{output_suffix}.txt',
        output_format=output_format
    )

if __name__ == "__main__":
     # Argument parser setup to handle command-line inputs for the master process
    parser = argparse.ArgumentParser(description="Master Process: Directory Fuzzing, Parameter Finding, and Payload Injection")
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads for fuzzing')
    parser.add_argument('-s', '--seconds', type=int, default=0, help='Seconds delay every 5 requests')
    parser.add_argument('-sc', '--statuscode', type=int, help='Status code to check (default: all status codes)')
    parser.add_argument('-H', '--headers', action='append', help='Custom Headers', default=[])
    parser.add_argument('-o', '--output', required=True, help='Output suffix for files')
    parser.add_argument('-of', '--outputformat', choices=['txt', 'json'], default='txt', help='Output format')
    
    # Parse the command-line arguments and run the master process with the provided parameters
    args = parser.parse_args()

    master_process(
        url=args.url,
        wordlist=args.wordlist,
        threads=args.threads,
        delay=args.seconds,
        status_code=args.statuscode,
        headers=parse_headers(args.headers),
        output_suffix=args.output,
        output_format=args.outputformat
    )
