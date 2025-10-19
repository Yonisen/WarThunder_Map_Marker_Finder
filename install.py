import subprocess
import sys


def install_dependencies():
    """
    Installs required Python packages from requirements.txt.
    """
    try:
        print("Installing dependencies from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\\nDependencies installed successfully.")
        print("You can now run the application by executing 'main.py' in the 'distance' directory.")
    except subprocess.CalledProcessError as e:
        print(f"\\nError installing dependencies: {e}")
        print("Please check your internet connection and try again.")
    except FileNotFoundError:
        print("\\nError: requirements.txt not found.")
        print("Please ensure the requirements.txt file is in the same directory as this script.")


if __name__ == "__main__":
    install_dependencies()
