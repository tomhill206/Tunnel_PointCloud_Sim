import numpy as np
import os
from scipy.stats import truncnorm

def generate_typical_tunnel_parameters(num_samples):

    # Empirical

    # Diameter limits
    #min_diameter, max_diameter = 5.5, 5.5

    #inner_diameter = np.linspace(min_diameter, max_diameter, num_samples)
    inner_diameter = np.full(num_samples, 5.5)
    width = np.full(num_samples, 1.2)
    num_segs = np.full(num_samples, 6)

    outer_diameter = (inner_diameter + 2*0.0085)/(1 - 2 * 0.0391)
    thickness = (outer_diameter - inner_diameter)/2

    """
    width_thickness_ratio = 20.38*np.exp(-outer_diameter/1.06) + 2.94 

    width =  width_thickness_ratio * thickness * 1.3
    """

    #num_segs = sample_number_of_segments(outer_diameter)
    

    radius = inner_diameter/2

    # Assumed relationships

    floor_height = 0.25 * radius
    platform_height = 0.6 * radius
    platform_width = 0.4 * radius
    platform_depth = platform_width / 10

    # Constants

    num_rings = np.full(num_samples, 20)
    rail_width = np.full(num_samples, 0.1)
    rail_height = np.full(num_samples, 0.1)
    rail_spacing = np.full(num_samples, 1)

    # Combining all parameters
    parameters = np.vstack((radius, num_segs, num_rings, thickness, width, floor_height, 
                            platform_height, platform_width, platform_depth,
                            rail_width, rail_height, rail_spacing)).T

    return parameters


def sample_number_of_segments(outer_diameters):
    
    num_segments_samples = []

    # Define the average and standard deviation for each diameter range
    diameter_ranges = {
        (0, 2): {'average': 5.68, 'std_dev': 0.50},
        (2, 4): {'average': 5.70, 'std_dev': 0.53},
        (4, 6): {'average': 6.16, 'std_dev': 0.43},
        (6, 8): {'average': 6.48, 'std_dev': 0.65},
        (8, 10): {'average': 7.73, 'std_dev': 0.80},
        (10, float('inf')): {'average': 9.13, 'std_dev': 0.74},
    }

    min_segments = 4
    # Sample the number of segments for each outer diameter based on its range
    for diameter in outer_diameters:
        for (min_diameter, max_diameter), stats in diameter_ranges.items():
            if min_diameter <= diameter < max_diameter:
                average = stats['average']
                std_dev = stats['std_dev']
                # Sample from a truncated normal distribution
                lower_bound = (min_segments - average) / std_dev
                upper_bound = float('inf')  # No upper truncation
                num_segments_dist = truncnorm(lower_bound, upper_bound, loc=average, scale=std_dev)
                num_segments = num_segments_dist.rvs(1).astype(int)
                num_segments_samples.append(num_segments[0])
                break

    return np.array(num_segments_samples)


def generate_and_save_parameters(N, output_dir):
    # Generate the typical tunnel parameters for N samples
    typical_params = generate_typical_tunnel_parameters(N)
    
    # Define ranges for the additional parameters (min, max)
    additional_ranges = {
        'wid_joi': (0.01, 0.02),  # Width of joint (float)
        'key_stone_small_arc': (10, 20),  # Key stone small arc angle (float)
        'key_stone_large_arc': (20, 25),  # Key stone large arc angle (float)
        'platform_side': (0, 1),  # Platform side (0 for 'L', 1 for 'R', integer range)
    }

    # Generate N sets of additional parameters
    additional_param_sets = []
    for _ in range(N):
        additional_params = {}
        for param, (low, high) in additional_ranges.items():
            if param == 'platform_side':  # platform_side is either 0 or 1
                additional_params[param] = np.random.choice([0, 1])
            else:
                additional_params[param] = np.random.uniform(low, high)
        additional_param_sets.append([additional_params[param] for param in additional_ranges])

    # Convert to 2D NumPy array
    additional_param_array = np.array(additional_param_sets)

    # Combine the typical parameters with the additional parameters
    combined_params = np.hstack((typical_params, additional_param_array))

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the generated parameters to a .npy file
    file_path = os.path.join(output_dir, 'parameter_sets.npy')
    np.save(file_path, combined_params)
    print(f"Saved parameters to {file_path}")

# Example usage
generate_and_save_parameters(1, 'data/numpy')


