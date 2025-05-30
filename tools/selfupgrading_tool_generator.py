
import os
import subprocess
import sys

def upgrade_self():
    try:
        # Check for the latest version
        output = subprocess.check_output('pip search self-upgrading-tool', shell=True)
        latest_version = output.split()[2]

        # Check the current version
        current_version = subprocess.check_output('pip show self-upgrading-tool', shell=True).split()[1].split(':')[1]

        # If the current version is not the latest, upgrade
        if current_version != latest_version:
            print('Upgrading to latest version...')
            os.system('pip install --upgrade self-upgrading-tool')
        else:
            print('You are using the latest version.')
    except Exception as e:
        print('Error occurred:', e)

if __name__ == '__main__':
    upgrade_self()
