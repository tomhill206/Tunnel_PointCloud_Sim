from utils.blend_executor import run_blender_script
from utils.clean_csv import process_csv

blender_path = '/Applications/Blender.app/Contents/MacOS/Blender'
blend_generator_script_path = '/Users/tomhill/Documents/Tunnel_PointCloud_Sim/blend_generator.py'
scanner_script_path = '/Applications/Blender.app/Contents/Resources/3.3/scripts/addons_contrib/range_scanner/scanner_script.py'
blend_file_path = '/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/blender/scene_temp_file.blend'


if __name__ == "__main__":
    # Create Blender file
    run_blender_script(blender_path, blend_generator_script_path)

    # Create csv file
    run_blender_script(blender_path, scanner_script_path, blend_file_path)

    process_csv('/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/pointclouds/tunnel1.csv')