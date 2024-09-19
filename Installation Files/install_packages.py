import os
import subprocess

# Directory where the packages were downloaded
download_dir = 'downloaded_packages'

# Define the order of installation
installation_order = [
    'pycparser',
    'cffi',
    'cryptography',
    'rstr',
    'pyglet',
    'pyparallel',
    'pylsl'
]

# Gather all the files in the download directory
files_in_directory = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith(('.whl', '.tar.gz'))]

# Sort the files based on the installation order
files_sorted = sorted(files_in_directory, key=lambda x: installation_order.index(next((pkg for pkg in installation_order if pkg in x), 'zzz')))

# Install each file
for file in files_sorted:
    print(f"Installing {file}...")
    command = f"pip install {file} --no-index --find-links={download_dir}"
    subprocess.check_call(command, shell=True)

print("Installation completed.")
