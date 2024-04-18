import os
import re

import argparse
import pandas as pd
import paramiko


class DiskUsage:
    """
    This class is used to calculate the disk usage of a directory tree on remote machine.

    """

    def __init__(self, arguments):
        """
        Initialize the DiskUsage class

        """
        if arguments.ssh_username:
            self.ssh_username = arguments.ssh_username
        else:
            # get the username from the environment variable
            self.ssh_username = os.environ.get('USER', None)
        if arguments.host:
            host = arguments.host
        else:
            # get the host from the environment variable
            host = os.environ.get('HOST', None)
        if arguments.ssh_password:
            self.ssh_password = arguments.ssh_password
        else:
            # get the password from the environment variable
            self.ssh_password = os.environ.get('PASSWORD', None)
        if not self.ssh_username or not self.ssh_host or not self.ssh_password:
            raise ValueError('Please provide the user, host, and password')
        self.limit = 10
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.current_path = os.path.join(self.current_path, 'disk_usage')
        os.makedirs(self.current_path, exist_ok=True)

    def get_details(self, path):
        """
        This method is used to get the children details of a parent directory on remote machine.

        :param path: The path of the parent directory.
        :type path: str
        """
        if self.ssh.get_transport().is_active():
            print(f'Getting the children details of the parent directory')
            command = f'echo {self.ssh_password} | sudo -S du -h --max-depth=5 {path}/* | sort -hr'
            stdin, stdout, stderr = self.ssh.exec_command(command)
            disk_usage = stdout.read().decode('utf-8')
            lines = disk_usage.split('\n')
            if len(lines) == 0:
                return [path]

            results = []
            for line in lines:
                if len(line) > 0:
                    # check if the line has a digit and the digit is greater than 10 and the line has M or G
                    if (re.search(r'M', line) and int(re.search(r'\d+', line).group()) > 10) \
                            or (re.search(r'G', line) and int(re.search(r'\d+', line).group()) > 0):
                        results.append(line.split('\t'))

            return results

    def get_disk_usage(self):
        """
        This method is used to get the disk usage of a directory tree on remote machine.

        :param path: The path of the directory tree.
        :type path: str

        :return: The disk usage of the directory tree.
        :rtype: int
        """
        print(f'Connecting to {self.ssh_host}')
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ssh_host, username=self.ssh_username, password=self.ssh_password)
        print(f'Connected to {self.ssh_host}')
        df = pd.DataFrame()
        if self.ssh.get_transport().is_active():
            print(f'Getting the disk usage of the directory tree')
            command = f'echo {self.ssh_password} | sudo -S du -sh /* | sort -hr'
            stdin, stdout, stderr = self.ssh.exec_command(command)
            disk_usage = stdout.read().decode('utf-8')
            # until you get the file name from the remote server increase the depth
            lines = disk_usage.split('\n')
            if len(lines) == 0:
                return
            final_results = []
            df = pd.DataFrame(columns=['Path', 'Size'])
            for index in range(0, self.limit):

                path = lines[index].split('\t')
                if len(path) == 1:
                    break
                print(path[1])
                results = self.get_details(path[1])
                for result in results:
                    if (re.search(r'M', result[0]) and int(re.search(r'\d+', result[0]).group()) > 10) \
                            or (re.search(r'G', result[0]) and int(re.search(r'\d+', result[0]).group()) > 0):
                        df = pd.concat([df, pd.DataFrame({'Path': [result[1]], 'Size': [result[0]]})])

            df = df.reset_index(drop=True)
            df = df.sort_values(by='Path')
            if os.path.exists(os.path.join(self.current_path, 'disk_usage.xlsx')):
                os.remove(os.path.join(self.current_path, 'disk_usage.xlsx'))
            df = df.reset_index(drop=True)
            df = df.drop_duplicates(subset=['Path', 'Size'], keep='first')
            df.to_excel(os.path.join(self.current_path, 'disk_usage.xlsx'), index=False)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--user', type=str, help='The username to connect to the remote server', default=None)
    arg_parser.add_argument('--host', type=str, help='The host to connect to', default=None)
    arg_parser.add_argument('--password', type=str, help='The password to connect to the remote server', default=None)
    arg_parser.add_argument('--dir', type=str, help='The directory to save the log file', default='logs')
    arg_parser.add_argument('--limit', type=int, help='The limit to get the disk usage', default=10)
    args = arg_parser.parse_args()
    Disk_Usage = DiskUsage(args)
    Disk_Usage.get_disk_usage()