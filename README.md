# War Thunder Map Marker Rangefinder

This tool provides an in-game rangefinder for War Thunder by analyzing screenshots of the minimap. It uses a YOLOv5 neural network to detect the player's tank and the yellow map marker, calculating the distance and azimuth between them. The application runs on any Windows 10 computer and relies on CPU for all computations.

## Features

-   **Accurate Rangefinding**: Calculates the distance to a map marker with an accuracy of ±20 meters.
-   **Customizable Overlay**: Display the distance and azimuth in a configurable overlay window.
-   **Easy to Use**: Set up the tool once and measure distances with a single hotkey.
-   **Screen Resolution Support**: Supports a wide range of screen resolutions.

## Installation

1.  **Install Python**:
    -   Download and install Python 3.13 from the [official website](https://www.python.org/).
    -   **Important**: During installation, make sure to check the box that says "Add Python to PATH."

2.  **Download the Project**:
    -   Download the project files by clicking the green "Code" button and selecting "Download ZIP."
    -   Extract the archive to a location of your choice.

3.  **Install Dependencies**:
    -   Open a command prompt or terminal in the project's root directory.
    -   Run the installation script by typing `python install.py` and pressing Enter. This will install all the necessary libraries.

## How to Use

1.  **Configure In-Game Settings**:
    -   Set your game to "Windowed Fullscreen" mode.
    -   Set the minimap size to the largest possible value.
    -   Assign a hotkey for the "squad marker" in the game's controls.

2.  **Configure the Tool**:
    -   Navigate to the `distance` directory and run `settings.pyw`.
    -   Select your screen resolution and configure the hotkeys for measuring distance and setting the map scale.
    -   You can also customize the position and transparency of the overlay.
    -   Click "Apply" to save your settings.

3.  **Run the Rangefinder**:
    -   In the `distance` directory, run `miniKarta.py`. A console window will appear, indicating that the program is running.
    -   Once in a match, open the minimap and use the "scale" hotkey to set the map scale.
    -   To measure the distance to a target, place the squad marker on it and press the "distance" hotkey. The range and azimuth will appear in the overlay.

## How It Works

The tool captures a screenshot of the minimap and uses a YOLOv5 model to identify the player's tank icon and the yellow squad marker. It then calculates the pixel coordinates of these two points and uses the map scale to determine the actual in-game distance and azimuth.
