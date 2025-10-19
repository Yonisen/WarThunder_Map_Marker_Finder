import os
import sys
import time
import traceback
from multiprocessing import Process, Queue
from subprocess import Popen
from threading import Timer

import torch

# Add the 'code' directory to the system path to allow importing modules from it
sys.path.append('code/')


def run_signal_process(queue, signal_module, pid_file):
    """
    Initializes and runs a signal process in a separate process.

    Args:
        queue (multiprocessing.Queue): The queue for inter-process communication.
        signal_module (str): The name of the signal module to import and run.
        pid_file (str): The path to the file where the process ID will be stored.
    """
    try:
        module = __import__(signal_module)
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        module.run(queue)  # Assuming each signal module has a 'run' function
    except Exception:
        with open('error.log', 'a') as f:
            f.write(f"\\n\\nError in {signal_module}:\\n")
            traceback.print_exc(file=f, chain=True)
        traceback.print_exc()


def run_print_results_process(queue):
    """
    Initializes and runs the printResults process.

    Args:
        queue (multiprocessing.Queue): The queue for inter-process communication.
    """
    try:
        import printResults
        with open('code/pid5.txt', 'w') as f:
            f.write(str(os.getpid()))
        printResults.printResults(queue)
    except Exception:
        with open('error.log', 'a') as f:
            f.write("\\n\\nError in printResults:\\n")
            traceback.print_exc(file=f, chain=True)
        traceback.print_exc()


class ProcessManager:
    """
    Manages the lifecycle of child processes for handling signals and results.
    """

    def __init__(self):
        self.signal_queue = None
        self.results_queue = None
        self.signal_process1 = None
        self.signal_process3 = None
        self.results_process = None
        self.start_child_processes()

    def start_child_processes(self):
        """
        Starts the child processes for handling signals and printing results.
        """
        self.signal_queue = Queue()
        self.results_queue = Queue()

        self.signal_process1 = Process(target=run_signal_process,
                                       args=(self.signal_queue, 'signal1', 'code/pid1.txt'))
        self.signal_process3 = Process(target=run_signal_process,
                                       args=(self.signal_queue, 'signal3', 'code/pid3.txt'))
        self.results_process = Process(target=run_print_results_process, args=(self.results_queue,))

        self.signal_process1.start()
        self.signal_process3.start()
        self.results_process.start()
        self.monitor_child_processes()

    def monitor_child_processes(self):
        """
        Monitors the health of child processes and restarts them if they fail.
        """
        if not all(p.is_alive() for p in [self.signal_process1, self.signal_process3, self.results_process]):
            print("One or more child processes have exited. Restarting...")
            # Cleanly terminate existing processes before restarting
            for p in [self.signal_process1, self.signal_process3, self.results_process]:
                if p.is_alive():
                    p.terminate()
                    p.join()
            self.start_child_processes()
            self.signal_queue.put("skip")  # Prevent processing of old messages
        else:
            Timer(0.1, self.monitor_child_processes).start()

    def get_signal_queue(self):
        return self.signal_queue

    def get_results_queue(self):
        return self.results_queue


def main():
    """
    Main function to initialize the application, load the model, and handle user input.
    """
    try:
        # Store the main process ID
        with open('code/pid.txt', 'w') as f:
            f.write(str(os.getpid()))

        print("Initializing the neural network...")

        # Load the YOLOv5 model from a local ONNX file
        model = torch.hub.load('code/yolo5', 'custom', 'code/yolo5/best.onnx', source='local')
        # The model runs on the CPU by default

        process_manager = ProcessManager()
        signal_queue = process_manager.get_signal_queue()
        results_queue = process_manager.get_results_queue()

        print("\\nWaiting for key combinations...")

        while True:
            message = signal_queue.get()
            if message == "distance":
                print("Calculating distance...")
                results_queue.put(['clear'])
                time.sleep(0.3)  # Wait for the UI to update
                import distanceFinder
                distanceFinder.checkDistance(model, results_queue)
            elif message == "scale":
                print("Opening scale settings...")
                Popen(["python", 'code/scale.py'])
            elif message == "skip":
                continue

    except Exception:
        with open('error.log', 'a') as f:
            f.write("\\n\\nAn unexpected error occurred in the main process:\\n")
            traceback.print_exc(file=f, chain=True)
        traceback.print_exc()


if __name__ == "__main__":
    main()
