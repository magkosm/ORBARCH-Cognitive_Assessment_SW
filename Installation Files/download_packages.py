import os
import subprocess

# List of packages you want to download
packages = ['pyglet==1.5.26', 'pyparallel==0.2.2', 'rstr==3.1.0', 'pylsl==1.16.1', 'cryptography==41.0.4', 'cffi==1.16.0', 'pycparser==2.21']

# Create a directory to store the downloaded packages
download_dir = 'downloaded_packages'
os.makedirs(download_dir, exist_ok=True)

# Download each package
for package in packages:
    print(f"Downloading {package} and its dependencies...")
    command = f"pip download {package} -d {download_dir}"
    subprocess.check_call(command, shell=True)

print("Download completed.")
