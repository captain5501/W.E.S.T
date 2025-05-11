import argparse
import time
from modules.banner import display_banner
from modules.directory_fuzzer import directory_fuzzer
from modules.parameter_finder import parameter_finder
from modules.injector import inject_params
from modules.utils import parse_headers
import subprocess
from PWEST import run_plugin_scan  # Import the function to run the plugin scan

def main():
    """
    Main function to parse command-line arguments and invoke the appropriate module functionality.
    This script serves as the entry point for the WordPress & its Eco-system Security Tool (WEST).
    """

    # Record the start time of the script
    start_time = time.time()

    # Initialize the argument parser with a description of the tool.
    parser = argparse.ArgumentParser(description="Below are the sub-commands to use for specific purposes:")
    
    # Create subparsers for different command-line commands.
    subparsers = parser.add_subparsers(dest='command')

    # Display the banner for the tool.
    display_banner()

    # ----------------------------
    # Directory Fuzzer Subcommand
    # ----------------------------
    # This subcommand handles the directory fuzzing functionality.
    dfuzz_parser = subparsers.add_parser('dfuzz', help='Directory Fuzzing')
    dfuzz_parser.add_argument('-u', '--url', required=True, help='Target URL')
    dfuzz_parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file for fuzzing directories')
    dfuzz_parser.add_argument('-t', '--threads', type=int, help='Number of threads for fuzzing to improve speed')
    dfuzz_parser.add_argument('-s', '--seconds', type=int, help='Seconds delay every 5 requests to avoid detection')
    dfuzz_parser.add_argument('-sc', '--statuscode', type=int, help='Specific status code to check (default: all status codes)')
    dfuzz_parser.add_argument('-H', '--headers', action='append', help='Custom headers to include in requests', default=[])
    dfuzz_parser.add_argument('-o', '--output', help='Output file to save the results')
    dfuzz_parser.add_argument('-of', '--outputformat', choices=['txt', 'json'], default='txt', help='Format of the output (text or JSON)')
    dfuzz_parser.add_argument('-e', '--errorfile', default='error.txt', help='Error output file (default: error.txt)')

    # ----------------------------
    # Parameter Finder Subcommand
    # ----------------------------
    # This subcommand handles finding parameters in a list of URLs.
    param_parser = subparsers.add_parser('param', help='Parameter Finder')
    param_parser.add_argument('-f', '--file', required=True, help='File containing a list of URLs to search for parameters')
    param_parser.add_argument('-o', '--output', help='Output file to save the found parameters')
    param_parser.add_argument('-of', '--outputformat', choices=['txt', 'json'], default='txt', help='Format of the output (text or JSON)')

    # ----------------------------
    # Injector Subcommand
    # ----------------------------
    # This subcommand handles injecting payloads into identified parameters.
    inject_parser = subparsers.add_parser('inject', help='Parameter Injection')
    inject_parser.add_argument('-t', '--target', required=True, help='File containing URLs with parameters to test')
    inject_parser.add_argument('-p', '--payload', required=True, help='File containing payloads for injection testing')
    inject_parser.add_argument('-o', '--output', help='Output file to save injection results')
    inject_parser.add_argument('-of', '--outputformat', choices=['txt', 'json'], default='txt', help='Format of the output (text or JSON)')

    # ----------------------------
    # Master Process Subcommand
    # ----------------------------
    # This subcommand handles the master process for directory fuzzing, parameter finding, and payload injection.
    master_parser = subparsers.add_parser('master', help='Master Process: Directory Fuzzing, Parameter Finding, and Payload Injection')
    master_parser.add_argument('-u', '--url', required=True, help='Target URL')
    master_parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file for fuzzing')
    master_parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads for fuzzing')
    master_parser.add_argument('-s', '--seconds', type=int, default=0, help='Seconds delay every 5 requests')
    master_parser.add_argument('-sc', '--statuscode', type=int, help='Specific status code to check (default: all status codes)')
    master_parser.add_argument('-H', '--headers', action='append', help='Custom Headers', default=[])
    master_parser.add_argument('-o', '--output', required=True, help='Output suffix for files')
    master_parser.add_argument('-of', '--outputformat', choices=['txt', 'json'], default='txt', help='Format of the output (text or JSON)')

    # ----------------------------
    # Plugin Subcommand
    # ----------------------------
    # This subcommand handles running the PHP vulnerability scanner.
    plugin_parser = subparsers.add_parser('plugin', help='Run PHP Vulnerability Scanner')
    plugin_parser.add_argument('path', type=str, help='Path to the folder containing PHP files to scan.')
    plugin_parser.add_argument('--xss', action='store_true', help='Enable scanning for XSS vulnerabilities.')
    plugin_parser.add_argument('--sql', action='store_true', help='Enable scanning for SQL injection vulnerabilities.')
    plugin_parser.add_argument('--custom', action='store_true', help='Scan the files for Custom Patterns')
    plugin_parser.add_argument('-o', '--output', type=str, help='Output file path for results (txt or json).')
    plugin_parser.add_argument('--log', action='store_true', help='Log vulnerabilities to vulnerabilities.log')

    # Parse the arguments provided by the user.
    args = parser.parse_args()

    # Execute the corresponding function based on the command-line subcommand chosen by the user.
    if args.command == 'dfuzz':
        # Parse custom headers from the command-line arguments.
        threads = args.threads if args.threads is not None else 10
        delay = args.seconds if args.seconds is not None else 0
        print(f"[INFO] Starting Directory Fuzzer with {threads} threads")
        headers = parse_headers(args.headers)
        # Invoke the directory fuzzer with the provided arguments.
        directory_fuzzer(
            url=args.url,
            wordlist=args.wordlist,
            threads=threads,
            delay=delay,
            status_code=args.statuscode,
            headers=headers,
            output=args.output,
            output_format=args.outputformat,
            error_output=args.errorfile
        )
    elif args.command == 'param':
        # Invoke the parameter finder with the provided arguments.
        parameter_finder(
            file=args.file,
            output=args.output,
            output_format=args.outputformat
        )
    elif args.command == 'inject':
        # Invoke the injection module with the provided arguments.
        inject_params(
            param_file=args.target,
            payload_file=args.payload,
            output=args.output,
            output_format=args.outputformat
        )
    elif args.command == 'master':
        # Build the command to run the master process module
        cmd = [
            'python', 'master_process.py',
            '-u', args.url,
            '-w', args.wordlist,
            '-t', str(args.threads),
            '-s', str(args.seconds),
            '-of', args.outputformat
        ]

        if args.statuscode:
            cmd += ['-sc', str(args.statuscode)]
        
        if args.headers:
            cmd += ['-H'] + args.headers
        
        cmd += ['-o', args.output]
        
        # Run the master process script using the constructed command
        subprocess.run(cmd)
    elif args.command == 'plugin':
        # Run the PHP vulnerability scanner with the provided arguments.
        run_plugin_scan(
            path=args.path,
            xss=args.xss,
            sql=args.sql,
            custom=args.custom,
            output=args.output,
            log=args.log
        )
    else:
        # If no valid subcommand is provided, print the help message.
        parser.print_help()

    # Record the end time of the script
    end_time = time.time()

    # Calculate the elapsed time in seconds
    elapsed_time = end_time - start_time

    # Print the total time taken to execute the script
    print(f"[INFO] Script completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
