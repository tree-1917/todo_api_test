# TODO List for SQLite Download Tutorial

1. **Download SQLite**
   - Go to the SQLite [download page](https://www.sqlite.org/download.html).
   - Download the `sqlite-tools-win32-x86-*.zip` file under "Precompiled Binaries for Windows".

2. **Extract SQLite**
   - Locate the downloaded ZIP file (usually in the Downloads folder).
   - Extract the contents to a folder (e.g., `C:\sqlite`).

3. **Move SQLite to `C:\`**
   - Cut the extracted `sqlite` folder.
   - Navigate to `C:\` in File Explorer.
   - Paste the `sqlite` folder into the root directory (`C:\`).

4. **Add SQLite to System PATH**
   - Right-click on "This PC" and select "Properties".
   - Click on "Advanced system settings".
   - In the System Properties window, click on "Environment Variables...".
   - Under "System variables", find and select the `Path` variable.
   - Click "Edit...".
   - Click "New" and add `C:\sqlite` (or the path to your SQLite folder).
   - Click "OK" to close all windows.

5. **Verify Installation**
   - Open Command Prompt (`cmd`).
   - Type `sqlite3 --version` and press Enter.
   - Verify that SQLite version information is displayed, indicating successful installation.

### Explanation

- **Download SQLite**: Obtain the SQLite binaries from the official website.
- **Extract SQLite**: Unzip the downloaded file to a location on your computer.
- **Move SQLite to `C:\`**: Transfer the extracted folder to the root directory of your C drive.
- **Add SQLite to System PATH**: Modify the system PATH variable to include the SQLite folder.
- **Verify Installation**: Ensure that SQLite is correctly installed and accessible from the Command Prompt.

