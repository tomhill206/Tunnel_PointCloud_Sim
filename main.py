from utils.blend_executor import run_blender_script
from utils.process_csv import clean_csv
from parameter_generator import generate_and_save_parameters
import os
import time

blender_path = '/Applications/Blender.app/Contents/MacOS/Blender'
blend_generator_script_path = '/Users/tomhill/Documents/Tunnel_PointCloud_Sim/blend_generator.py'
scanner_script_path = '/Applications/Blender.app/Contents/Resources/3.3/scripts/addons_contrib/range_scanner/scanner_script.py'
blend_file_path = '/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/blender/tunnel.blend'

def wait_for_file(file_path, timeout=None):
    """
    Waits for a file to appear at the specified path.

    :param file_path: Path to the file to wait for.
    :param timeout: Maximum time to wait in seconds. If None, waits indefinitely.
    :return: True if the file appeared, False if timed out.
    """
    start_time = time.time()

    while True:
        # Check if file exists
        if os.path.exists(file_path):
            return True

        # If a timeout is specified, check if the timeout has been exceeded
        if timeout and (time.time() - start_time) > timeout:
            print(f"Timeout exceeded while waiting for file: {file_path}")
            return False

        print('Waiting for scan to appear....')
        # Wait for a short period before checking again
        time.sleep(1)  # Sleep for 1 second


if __name__ == "__main__":

    N = 2

    generate_and_save_parameters(N, 'data/numpy')

    for i in range(N):

        # Create Blender file
        run_blender_script(blender_path, blend_generator_script_path)

        # Create csv file
        print(f'Scanning tunnel{i}....')
        run_blender_script(blender_path, scanner_script_path, blend_file_path)

        wait_for_file('data/csv/tunnel_frames_1_to_1.csv', timeout=60)

        clean_csv(f'data/pointclouds/tunnel{i}.csv')

        os.remove('data/csv/tunnel_frames_1_to_1.csv')
        os.remove('data/blender/tunnel.blend')