### `README.md`


# WEST: WordPress & Eco-system Security Tool

## Introduction

WEST is a comprehensive security tool designed for assessing the security of WordPress installations and their associated components. It offers functionalities for directory fuzzing, parameter discovery, payload injection, and plugin vulnerability scanning.

## Features

- **Directory Fuzzing**: Perform directory and file fuzzing on a target URL using a specified wordlist.
- **Parameter Discovery**: Extract and analyze parameters from a list of URLs.
- **Payload Injection**: Test for vulnerabilities by injecting payloads into identified parameters.
- **Master Process**: A unified command to execute directory fuzzing, parameter discovery, and payload injection sequentially.
- **Plugin Vulnerability Scanning**: Detect vulnerabilities such as XSS and SQL Injection in PHP files.

## Installation

To install the necessary dependencies, use the following command:

```bash
pip install -r requirements.txt
```

## Commands

### Directory Fuzzing

Use this command to start directory fuzzing:

```bash
python west.py dfuzz -u <target_url> -w <wordlist_file> [-t <threads>] [-s <seconds>] [-sc <status_code>] [-H <header>] [-o <output_file>] [-of <output_format>] [-e <error_file>]
```
## Arguments

- `-u`, `--url`: URL to target for directory fuzzing or master process.
- `-w`, `--wordlist`: Wordlist file used for directory fuzzing.
- `-t`, `--threads`: Number of threads for fuzzing.
- `-s`, `--seconds`: Delay in seconds between requests.
- `-sc`, `--statuscode`: Status code to filter results during fuzzing.
- `-H`, `--headers`: Custom headers to include in requests.
- `-o`, `--output`: Output file for saving results.
- `-of`, `--outputformat`: Format of the output file (txt or json).
- `-e`, `--errorfile`: File to save error messages.

### Parameter Discovery

Use this command to discover parameters from a list of URLs:

```bash
python west.py param -f <url_file> [-o <output_file>] [-of <output_format>]
```
## Arguments

- `-f`, `--file`: File containing a list of URLs to search for parameters
- `-o`, `--output`: Output file for saving results.
- `-of`, `--outputformat`: Format of the output file (txt or json).

### Payload Injection

Use this command to inject payloads into parameters:

```bash
python west.py inject -t <target_file> -p <payload_file> [-o <output_file>] [-of <output_format>]
```
## Arguments

- `-t`, `--target`: File containing URLs with parameters to test
- `-o`, `--output`: Output file for saving results.
- `-of`, `--outputformat`: Format of the output file (txt or json).

### Master Process

Run the master process to combine directory fuzzing, parameter discovery, and payload injection:

```bash
python west.py master -u <target_url> -w <wordlist_file> [-t <threads>] [-s <seconds>] [-sc <status_code>] [-H <header>] -o <output_suffix> [-of <output_format>]
```

## Arguments

- `-u`, `--url`: URL to target for directory fuzzing or master process.
- `-w`, `--wordlist`: Wordlist file used for directory fuzzing.
- `-t`, `--threads`: Number of threads for fuzzing.
- `-s`, `--seconds`: Delay in seconds between requests.
- `-sc`, `--statuscode`: Status code to filter results during fuzzing.
- `-H`, `--headers`: Custom headers to include in requests.
- `-o`, `--output`: Output file for saving results.
- `-of`, `--outputformat`: Format of the output file (txt or json).

### PLugin Vulnerability Scanning

To scan PHP files for vulnerabilities:

```bash
python west.py plugin <path_to_php_files> [--xss] [--sql] [--custom] [-o <output_file>] [--log]
```

## Arguments:

- `--xss`: Enable scanning for XSS vulnerabilities.
- `--sql`: Enable scanning for SQL Injection vulnerabilities.
- `--custom`: Enable scanning for custom vulnerabilities.
- `--log`: Log vulnerabilities to a file.

## License

To be Licensed in the future.

## Contributing

Contributions are encouraged! Please fork the repository and submit a pull request with your improvements.

## Contact

For questions or feedback, please raise an issue on the GitHub repository or reach out to captainp5501@gmail.com