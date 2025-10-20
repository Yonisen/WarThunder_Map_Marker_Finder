# WarThunder Map Marker Finder

This tool is a rangefinder for the game WarThunder, which works by taking a screenshot of the minimap and using a YOLOv5 model to identify the player's vehicle and a yellow map marker. It then calculates the distance and azimuth between the two points and displays the information in an overlay.

## Installation

1.  Download the repository as a ZIP file and extract it.
2.  Navigate to the `distance` directory.
3.  Run the `install.py` script to install the required Python packages.

## Usage

1.  Run the `miniKarta.py` script to start the application.
2.  The application will run in the background and wait for hotkey presses.
3.  The default hotkeys are:
    *   **t**: Measure the distance to the yellow marker.
    *   **Ctrl+N**: Set the map scale.

## How it Works

When the distance measurement hotkey is pressed, the application takes a screenshot of the minimap. The YOLOv5 model then analyzes the screenshot to find the player's vehicle and the yellow marker. Once both are found, the application calculates the distance and azimuth between them. The results are then displayed in a transparent overlay window.

## Configuration

The hotkeys and other settings can be configured in the `distance/code/buttons.ini` file.
