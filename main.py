from utils.blend_executor import run_blender_script
from utils.process_csv import clean_csv
from parameter_generator import generate_and_save_parameters
import os

blender_path = '/Applications/Blender.app/Contents/MacOS/Blender'
blend_generator_script_path = '/Users/tomhill/Documents/Tunnel_PointCloud_Sim/blend_generator.py'
scanner_script_path = '/Applications/Blender.app/Contents/Resources/3.3/scripts/addons_contrib/range_scanner/scanner_script.py'
blend_file_path = '/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/blender/tunnel.blend'


if __name__ == "__main__":

    N = 3

    generate_and_save_parameters(N, 'data/numpy')

    for i in range(N):

        # Create Blender file
        run_blender_script(blender_path, blend_generator_script_path)

        # Create csv file
        run_blender_script(blender_path, scanner_script_path, blend_file_path)

        clean_csv(f'data/pointclouds/tunnel{i}.csv')

        os.remove('data/csv/tunnel_frames_1_to_1.csv')
        os.remove('data/blender/tunnel.blend')