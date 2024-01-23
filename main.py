from utils.blend_executor import run_blender_script
from utils.process_data import clean_csv
from utils.read_config import read_config
from parameter_generator_emp import generate_and_save_parameters
import os
import time
import numpy as np

config = read_config('config.txt')

blender_path = config['blender_app_path'] + '/Contents/MacOS/Blender'
blend_generator_script_path = config['tunnel_pointcloud_sim_path'] + '/blend_generator.py'
scanner_script_path = config['blender_app_path'] + '/Contents/Resources/3.3/scripts/addons_contrib/range_scanner/scanner_script.py'
blend_file_path = config['tunnel_pointcloud_sim_path'] + '/data/blender/tunnel.blend'

if __name__ == "__main__":

    N = config['number_of_simulations']

    expected_scan_time = np.square(1/config['scanner_step_degree']) * 5

    generate_and_save_parameters(N, 'data/numpy')

    for i in range(N):

        # Create Blender file
        run_blender_script(blender_path, blend_generator_script_path)

        # Create csv file
        scanning_start_time = time.time()
        print(f'Scanning tunnel{i}....')
        print(f"Expected scan time: {expected_scan_time:.1f} seconds")
        run_blender_script(blender_path, scanner_script_path, blend_file_path)

        clean_csv(f'data/pointclouds/tunnel{i}.csv')

        os.remove('data/csv/tunnel_frames_1_to_1.csv')
        os.remove('data/blender/tunnel.blend')

        print(f'Time taken to scan pointcloud: {time.time() - scanning_start_time:.1f}')