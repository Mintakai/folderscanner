# folderscanner (is_deployed)

## Patchnotes

### 01.09.2023 Version a_3

- Added a field to input a specific filename, you're looking for.
  - For example if the url is "C:\Users\user\Desktop" and the filename is "test", User desktop will be scanned for:
    - test.deployed
    - test.isdeploying
    - test.failed
- Added a config file to save earlier folder and filename.
- Added a sound for moving from status to another.
  - From any status to [Deployed], smooth ping.
  - From any status to any, alert sound.
  - Mute feature incoming...
- Added info message that pops up during first startup.
  - Can be disabled by clicking "No".
  - If disabled, can be shown again by clicking the status area.

## Introduction

The **Is Deployed** is a simple GUI application built using Python's Tkinter library. It allows users to check the status of a specified folder and visually displays whether the folder contains specific files indicating deployment status.

- .deployed
  - The status area will be green and have text [DEPLOYED]

- .isdeploying
  - The status area will be yellow and have text [DEPLOYING]

- when neither is found
  - The status area will be light red and have text [DOWN]

- when .failed is found
  - The status area will be red and have text [FAILED]

### Images

Starting the app<br>
(Unlike in this image, when you have a folder selected, it'll show the time since it's entered the down -state)<br>
![startup](https://github.com/Mintakai/folderscanner/blob/main/docimg/startup.png)

Deployed status<br>
![deployed](https://github.com/Mintakai/folderscanner/blob/main/docimg/deployed.png)

Isdeploying status<br>
![isdeploying](https://github.com/Mintakai/folderscanner/blob/main/docimg/isdeploying.png)

Down status<br>
![down](https://github.com/Mintakai/folderscanner/blob/main/docimg/down.png)

Failed status<br>
![failed](https://github.com/Mintakai/folderscanner/blob/main/docimg/failed.png)

Info message<br>
(You can click "No" to stop showing this at startup.
Clicking on the status bar will pop this up at any time.)
![info](https://github.com/Mintakai/folderscanner/blob/main/docimg/info.png)

## Features

- Check the deployment status of a specified folder with a specific filename.
- Visual indication of deployment status through background colors and status text.
- Timestamp display of the last change in status.
- Remember last folder and filename.
- Play a sound when status changes.
- Info message at first startup (And concurrent ones, if not disabled).

## Usage

### Prerequisites

- Python 3.x
- Tkinter (usually included with Python)
- Pygame (This is required for the sounds)
- PyInstaller (for building the executable)

### Installation

1. Clone the repository to your local machine

2. Navigate to the project directory:

  ```

  cd is_deployed

  ```

3. Make sure you have pygame installed

  ```

  pip install pygame

  ```

4. Make sure you have pyinstaller installed

  ```

  pip install pyinstaller

  ```

5. Build the standalone executable using PyInstaller:

  ```

  pyinstaller --onefile --noconsole --add-data "sfx\ok.mp3;sfx" --add-data "sfx\error.mp3;sfx" .\is_deployed.py

  ```

- onefile: Generate a single standalone executable file.
- noconsole: Do not display a console window when the executable is run.
- add-data: Bundle the sfx files with the executable.

The built executable will be found in the dist directory.

### Running the App
Run the executable file (e.g., is_deployed.exe) located in the dist directory.

The app's GUI window will open.
Enter the path to the folder you want to check in the input field or click the "Browse" button to select the folder.
The app will automatically poll the status at regular intervals (default: 5000 milliseconds). You can adjust this interval by modifying the POLL_INTERVAL constant in the code.

## License
This project is licensed under the MIT License.
