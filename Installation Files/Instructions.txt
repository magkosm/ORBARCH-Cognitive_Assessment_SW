# Prerequisites

- **Administrator Access**: Some steps require administrator privileges.
- **OpenGL 2.0 Support**: Ensure your system supports OpenGL 2.0.

---

## 1. Extract the "Release for Ax-4" Folder

- **Locate the Downloaded File "Release for Ax-4.zip":**
  - Navigate to your **"Downloads"** folder.
  - Find the **"Release for Ax-4.zip"** file.

- **Move to Desktop:**
  - Drag and drop the **"Release for Ax-4.zip"** file from the Downloads folder to your **Desktop**.

- **Extract the Contents:**
  - Right-click on **"Release for Ax-4.zip"** on your Desktop.
  - Select **"Extract All..."** from the context menu.
  - Click **"Extract"** in the extraction window to extract the files to a new folder on your Desktop.
  - Once completed, close any open windows related to the extraction.

---

## 2. Install Python 3.9.11

- **Access Installation Files:**
  - Open the **"Release for Ax-4"** folder on your Desktop.
  - Inside, find the **"Installation Files"** folder.
  - Drag and drop the **"Installation Files"** folder to your **Desktop**.
  - Close the **"Release for Ax-4"** folder.

- **Run Python Installer:**
  - Open the **"Installation Files"** folder on your Desktop.
  - Double-click on **"python-3.9.11-amd64.exe"** to start the Python installation.

- **Customize Installation:**
  - In the installer window:
    - **Check** the box that says **"Add Python 3.9 to PATH"**.
    - Click on **"Customize installation"**.
    - **Optional Features Screen:**
      - Ensure all desired features are selected.
      - Click **"Next"**.
    - **Advanced Options Screen:**
      - **Check** **"Install for all users"** (this is probably necessary).
      - Ensure **"Add Python to environment variables"** is **selected**.
      - Click **"Install"** to begin the installation.
    - Wait for the installation to complete and then click **"Close"**.

---

## 3. Install Required Python Packages

- **Verify Package Contents:**
  - In the **"Installation Files"** folder, open the **"downloaded_packages"** folder to ensure all necessary packages are present.
  - Close the **"downloaded_packages"** folder to return to the **"Installation Files"** folder.

- **Run Package Installer:**
  - Locate the **"install_packages.bat"** file in the **"Installation Files"** folder.

  - **Run the Batch File:**
    - Right-click on **"install_packages.bat"**.
    - If a security warning appears (Windows Defender SmartScreen), click on **"More info"** and then select **"Run anyway"**.

  - A Command Prompt window will open and execute the script to install the required Python packages.

  - **Wait for Completion:**
    - Monitor the Command Prompt window until you see the message **"Installation Completed."**
    - When prompted, press any key to close the Command Prompt window.

---

## 4. Prepare Data Folders

- **Select Data Folders:**
  - In the **"Installation Files"** folder, locate the following folders:
    - **"FNIRS_Data"**
    - **"ORBARCH_Data"**
    - **"Configuration File for Cortiview"**
    - **"Orbital Architecture - SW - v.2.0"**

- **Move Folders to Desktop:**
  - Select all four folders (you can hold the **Ctrl** key and click each folder to select multiple items).
  - Drag and drop the selected folders to your **Desktop**.
  - Close the **"Installation Files"** folder.

---

## 5. Create Desktop Shortcuts for the Application

- **Navigate to Application Folder:**
  - Open the **"Orbital Architecture - SW - v.2.0"** folder on your Desktop.

- **Create Shortcut for Cognitive Assessment:**
  - Scroll to find the **"start_Cognitive_Assessment"** file (this might be a `.exe` or `.bat` file).
  - Right-click on **"start_Cognitive_Assessment"**.
  - Select **"Create shortcut"** from the context menu.

- **Create Shortcut for Encryption Tool:**
  - In the same folder, find **"encrypt_hybrid_fnirs.bat"**.
  - Right-click on **"encrypt_hybrid_fnirs.bat"**.
  - Select **"Create shortcut"**.

- **Move Shortcuts to Desktop:**
  - Drag and drop both shortcuts to your **Desktop**.

- **Optional - Rename the Shortcuts:**
  - Click on the shortcuts on your Desktop.
  - Press **F2** or right-click and select **"Rename"**.
  - Rename them to something like **"Start Cognitive Assessment"** and **"Encrypt FNIRS Data"** for easy identification.

- **Optional - Change Shortcut Icon:**
  - Right-click on the shortcut on your Desktop and select **"Properties"**.
  - Navigate to the **"Shortcut"** tab, and click **"Change Icon..."**.
  - If prompted with an instruction pop-up message, click **"OK"**.
  - Choose an icon from the list or browse for a custom icon file.
  - Click **"OK"**, then **"Apply"**, and finally **"OK"** to save the changes.

---

## 6. Set Up Encryption Keys (If Necessary) **NOT IN CURRENT DEPLOYMENT!**

- **Open the Encryption Files Folder:**
  - In the **"Orbital Architecture - SW - v.2.0"** folder, open the **"Encryption files"** folder.

- **Generate New Keys (Optional):**
  - If you need to generate a new set of public and private keys:
    - Locate the **"key_generation.bat"** file.
    - Double-click on **"key_generation.bat"** to run it.
    - This will generate new encryption keys.

- **Move Generated Keys:**
  - After key generation, distribute the keys appropriately:
    - **Public Key:**
      - Replace the existing public key in the **"encryption"** folder.
      - Replace the existing public key in the **"public_key"** folder within **"Orbital Architecture - SW - v.2.0"**.
    - **Private Key:**
      - Move the new private key to the **"decryption"** folder.

---

## 7. Using the Software

- **Start the Cognitive Assessment**

  - **Launch the Application:**
    - Double-click on the **"Start Cognitive Assessment"** shortcut on your Desktop.

  - **Controls During Assessment:**
    - **CTRL + N**: Skip to the next screen in segments with a black background.
    - **CTRL + Q**: Exit the segment completely.

- **Encrypting FNIRS Data**

  - **Prepare Data:**
    - Ensure your FNIRS data is in the **"FNIRS_Data"** folder on your Desktop.

  - **Run Encryption:**
    - Double-click on the **"Encrypt FNIRS Data"** shortcut on your Desktop.

  - **Outcome:**
    - An encrypted file will be generated on your Desktop upon completion.

---

## 8. Decrypting Files (If Necessary) **NOT IN CURRENT DEPLOYMENT!**

- **Decrypt Files:**
  - Move the encrypted files into the **"decrypt"** folder within the **"Orbital Architecture - SW - v.2.0"** folder.
  - Double-click on the **"decrypt.bat"** file to decrypt the files.

---

## 9. Uninstallation Instructions

### **Uninstalling the Cognitive Software and Associated Files**

1. **Delete Application Folders and Shortcuts:**

   - **Remove Shortcuts:**
     - Delete the **"Start Cognitive Assessment"** and **"Encrypt FNIRS Data"** shortcuts from your Desktop.

   - **Delete Folders:**
     - On your Desktop, locate and delete the following folders:
       - **"FNIRS_Data"**
       - **"ORBARCH_Data"**
       - **"Configuration File for Cortiview"**
       - **"Orbital Architecture - SW - v.2.0"**
       - **"Installation Files"** (if still present)
       - **"Release for Ax-4"** (if still present)

   - **Empty Recycle Bin:**
     - Right-click on the Recycle Bin and select **"Empty Recycle Bin"** to permanently remove the files.

### **Uninstalling Python 3.9.11**

2. **Uninstall Python:**

   - **Access Programs and Features:**
     - Press **Windows Key + R** to open the Run dialog box.
     - Type `appwiz.cpl` and press **Enter** to open **Programs and Features**.

   - **Locate Python Installation:**
     - Scroll through the list of installed programs and find **"Python 3.9.11 (64-bit)"**.

   - **Uninstall Python:**
     - Click on **"Python 3.9.11 (64-bit)"** to select it.
     - Click on **"Uninstall"** at the top of the program list.
     - Follow the prompts to complete the uninstallation.

3. **Remove Python from Environment Variables (If Necessary):**

   - **Access System Properties:**
     - Right-click on **"This PC"** or **"My Computer"** on your Desktop or in File Explorer.
     - Select **"Properties"**.
     - Click on **"Advanced system settings"**.

   - **Edit Environment Variables:**
     - In the **System Properties** window, click on the **"Environment Variables..."** button.
     - Under **"System variables"**, scroll to find **"Path"** and select it.
     - Click on **"Edit..."**.
     - Look for any entries related to **Python 3.9** or **Python39**.
     - Select the Python-related entries and click **"Delete"**.
     - Click **"OK"** to close each window.

### **Uninstalling Installed Python Packages**

4. **Remove Installed Packages (Optional):**

   - **Note:** Uninstalling Python typically removes associated packages. However, if you want to ensure all packages are removed:

   - **Delete Pip Cache (Optional):**
     - Open File Explorer.
     - Navigate to `%LocalAppData%\pip\Cache` (you can paste this path into the address bar).
     - Delete the contents of the **"Cache"** folder.

   - **Delete Python Folder in AppData (Optional):**
     - Navigate to `%LocalAppData%\Programs\Python` or `%AppData%\Python`.
     - Delete any remaining Python folders.

---

## Notes and Tips

- **Administrator Permissions:**
  - Some installation and uninstallation steps may require administrator rights. If prompted, enter your administrator password or contact your system administrator.

- **Security Warnings:**
  - Windows may display security warnings when running executables or batch files. Ensure you trust the source before proceeding.

- **Environment Variables:**
  - Adding Python to your PATH allows you to run Python from the Command Prompt. This was enabled during the Python installation.

- **Verifying Installations:**
  - To verify Python installation, open Command Prompt and type `python --version`. It should display **Python 3.9.11**.
  - After uninstallation, typing `python --version` should result in an error or message indicating Python is not recognized.

- **Troubleshooting:**
  - If you encounter issues during package installation, ensure that you have the latest version of pip by running `python -m pip install --upgrade pip`.

- **Restart Your Computer:**
  - After uninstalling, it's a good idea to restart your computer to ensure all changes take effect.

---

By following these instructions, you should have successfully installed or uninstalled the Cognitive Software, Python 3.9.11, and all associated packages on your computer.

If you decide to reinstall the software in the future, you can follow the installation instructions provided above.

---
