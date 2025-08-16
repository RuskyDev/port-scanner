# Port Scanner
A super-fast port scanner tool written in pure Python with no extra dependencies and various customizable options.

## Features
- Scan a range of ports on any target host
- Supports high concurrency
- Customizable timeout
- Displays progress while scanning

## Requirements
- Python 3.8+
- No external dependencies

## Usage
```bash
$ python3 main.py <target> [--start START_PORT] [--end END_PORT] [--concurrency N] [--timeout SECONDS] [--ipv6]
````

## Example
```bash
$ python3 main.py 127.0.0.1 --start 1 --end 1000 --concurrency 200 --timeout 0.3
```

## Disclaimer
This tool was created for penetration testing and educational purposes only. I take no responsibility for how this script is used.
