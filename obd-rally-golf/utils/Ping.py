import subprocess

class Ping:
    def __init__(self, host="8.8.8.8", count=1, timeout=1):
        self.host = host
        self.count = count
        self.timeout = timeout

    def check_connection(self):
        """
        Pings the specified host to check for an internet connection.

        :return: True if the internet connection is available, False otherwise.
        """
        try:
            # Build the ping command based on the operating system
            command = ["ping", "-c", str(self.count), "-W", str(self.timeout), self.host]
            # Execute the ping command
            subprocess.check_output(command, stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            print("No internet connection.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
