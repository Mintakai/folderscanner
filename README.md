# folderscanner (is_deployed)

The **Is Deployed** is a simple GUI application built using Python's Tkinter library. It allows users to check the status of a specified folder and visually displays whether the folder contains specific files indicating deployment status.

- .deployed
  - The status area will be green and have text [DEPLOYED]

- .isdeploying
  - The status area will be yellow and have text [DEPLOYING]

- when neither is found
  - The status area will be red and have text [DOWN]

## Features

- Check the deployment status of a specified folder.
- Visual indication of deployment status through background colors and status text.
- Timestamp display of the last change in status.

## Usage

### Prerequisites

- Python 3.x
- Tkinter (usually included with Python)

### Installation

1. Clone the repository to your local machine

2. Navigate to the project directory:

   ```

   cd is_deployed

   ```
3. Build the standalone executable using PyInstaller:

   ```

   pyinstaller --onefile --noconsole .\is_deployed.py

   ```

- onefile: Generate a single standalone executable file.
- noconsole: Do not display a console window when the executable is run.

The built executable will be found in the dist directory.

### Running the App
Run the executable file (e.g., is_deployed.exe) located in the dist directory.

The app's GUI window will open.
Enter the path to the folder you want to check in the input field or click the "Browse" button to select the folder.
The app will automatically poll the status at regular intervals (default: 5000 milliseconds). You can adjust this interval by modifying the POLL_INTERVAL constant in the code.

## License
This project is licensed under the MIT License.
