import numpy as np
import os

def generate_and_save_parameters(N, output_dir):
    # Define ranges for each parameter (min, max)
    ranges = {
        'r': (2.5, 5),  # Radius (float)
        'num_segs': (3, 10),  # Number of segments (integer range)
        'num_rings': (20, 21),  # Always 20
        'wid_joi': (0.01, 0.02),  # Width of joint (float)
        'dep_joi': (0.04, 0.06),  # Depth of joint (float)
        'len_seg': (1.0, 2.0),  # Length of segment (float)
        'key_stone_small_arc': (10, 20),  # Key stone small arc angle (float)
        'key_stone_large_arc': (20, 25),  # Key stone large arc angle (float)
        'floor_height': (0.3, 0.7),  # Floor height (float)
        'platform_height': (1.0, 2.0),  # Platform height (float)
        'platform_width': (1.0, 1.5),  # Platform width (float)
        'platform_depth': (0.05, 0.15),  # Platform depth (float)
        'platform_side': (0, 1),  # Platform side (0 for 'L', 1 for 'R', integer range)
        'rail_width': (0.05, 0.15),  # Rail width (float)
        'rail_height': (0.1, 0.2),  # Rail height (float)
        'rail_spacing': (0.9, 1.5),  # Rail spacing (float)
    }

    # Generate N sets of parameters
    param_sets = []
    for _ in range(N):
        params = {}
        for param, (low, high) in ranges.items():
            if param in ['num_segs', 'num_rings', 'platform_side']:
                params[param] = np.random.randint(low, high + 1) # randint not inclusive
            else:
                params[param] = float(np.random.uniform(low, high))
        param_sets.append([params[param] for param in ranges])

    # Convert to 2D NumPy array
    param_array = np.array(param_sets)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the generated parameters to a .npy file
    file_path = os.path.join(output_dir, 'parameter_sets.npy')
    np.save(file_path, param_array)
    print(f"Saved parameters to {file_path}")

# Example usage
#generate_and_save_parameters(3, 'data/numpy')
