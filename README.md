# Disk Usage Analyzer

> This Python script is used to calculate the disk usage of a directory tree on a remote machine. It uses SSH for remote connection and access.

## Requirements

- Python 3.6+
- Libraries: os, re, argparse, pandas, paramiko

## Usage

> > You can use this script by providing the necessary arguments while running the script. Here is an example:

```bash
python disk_usage.py --ssh_username your_username --host your_host --ssh_password your_password
```
## Arguments

- `--ssh_username`: The username for the SSH connection. If not provided, the script will try to get it from the USER environment variable.
- `--host`: The host for the SSH connection. If not provided, the script will try to get it from the HOST environment variable.
- `--ssh_password`: The password for the SSH connection. If not provided, the script will try to get it from the PASSWORD environment variable.

> > If the script cannot find the necessary information (username, host, password), it will raise a ValueError.

## Contributing

> > Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Arguments
- - ssh_username: The username for the SSH connection. If not provided, the script will try to get it from the USER environment variable.
- - host: The host for the SSH connection. If not provided, the script will try to get it from the HOST environment variable.
- - ssh_password: The password for the SSH connection. If not provided, the script will try to get it from the PASSWORD environment variable.

## NOTE*: 
 > If the script cannot find the necessary information (username, host, password), it will raise a ValueError.
