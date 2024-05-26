import subprocess

class Systemctl:
    def __init__(self):
        pass

    def check_service_status(self, service_name):
        try:
            # Execute the systemctl command to get the status of the service
            result = subprocess.run(['systemctl', 'is-active', service_name],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            
            # The command returns 'active' if the service is running
            if result.stdout.strip() == 'active' or result.stdout.strip() == 'activating':
                return True
        except subprocess.CalledProcessError as e:
            # Handle the error case where the systemctl command fails
            print(f"Error checking status of service {service_name}: {e}")
        
        return False
