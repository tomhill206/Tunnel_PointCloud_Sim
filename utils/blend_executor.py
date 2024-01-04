import subprocess
import os

def run_blender_script(blender_path, script_path, blender_file=None, args=None):
    """
    Runs a Blender script using subprocess.

    :param blender_path: Path to the Blender executable.
    :param script_path: Path to the Python script to be executed in Blender.
    :param blender_file: (Optional) Path to a .blend file to be loaded.
    :param args: (Optional) Additional arguments to be passed to the script.
    :return: None
    """

    # Construct the basic command
    command = [blender_path, '--background']

    # Add the Blender file if provided
    if blender_file:
        command.append(blender_file)

    # Add the Python script execution command
    command.extend(['--python', script_path])

    # Add any additional arguments
    if args:
        command.extend(args)

    try:
        # Execute the command and capture output
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Log the output and errors
        print("Blender Script Output:")
        print(result.stdout)
        if result.stderr:
            print("Blender Script Errors:")
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Blender script: {script_path}")
        print(e)

# Example usage:
# run_blender_script('/path/to/blender', '/path/to/script.py', '/path/to/file.blend', ['--some', '--additional', 'args'])
