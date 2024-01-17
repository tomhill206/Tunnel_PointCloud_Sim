import numpy as np
import os
from scipy.stats import truncnorm

def generate_typical_tunnel_parameters(num_samples):

    # Empirical

    # Diameter
    mean_diameter, std_diameter = 3.14, 1.61
    min_diameter, max_diameter = 1.14, 13.2  # Truncation limits

    # Sampling Outer Diameter from truncated Gaussian distribution
    outer_diameter_dist = truncnorm(
        (min_diameter - mean_diameter) / std_diameter,
        (max_diameter - mean_diameter) / std_diameter,
        loc=mean_diameter,
        scale=std_diameter
    )
    outer_diameter = outer_diameter_dist.rvs(num_samples)

    thickness = 0.0085 + 0.0391 * outer_diameter

    width_thickness_ratio = 20.38*np.exp(-outer_diameter/1.06) + 2.94

    width =  width_thickness_ratio * thickness

    num_segs = sample_number_of_segments(outer_diameter)

    radius = outer_diameter/2 - thickness

    # Assumed relationships

    floor_height = 0.25 * radius
    platform_height = 0.6 * radius

    # Combining all parameters
    parameters = np.vstack((num_segs, thickness, radius, width, floor_height, platform_height)).T

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
        'num_rings': (20, 20),  # Always 20
        'wid_joi': (0.01, 0.02),  # Width of joint (float)
        'key_stone_small_arc': (10, 20),  # Key stone small arc angle (float)
        'key_stone_large_arc': (20, 25),  # Key stone large arc angle (float)
        'platform_width': (1.0, 1.5),  # Platform width (float)
        'platform_depth': (0.05, 0.15),  # Platform depth (float)
        'platform_side': (0, 1),  # Platform side (0 for 'L', 1 for 'R', integer range)
        'rail_width': (0.05, 0.15),  # Rail width (float)
        'rail_height': (0.1, 0.2),  # Rail height (float)
        'rail_spacing': (0.9, 1.5),  # Rail spacing (float)
    }

    # Generate N sets of additional parameters
    additional_param_sets = []
    for _ in range(N):
        additional_params = {}
        for param, (low, high) in additional_ranges.items():
            if param == 'num_rings':  # num_rings is always 20
                additional_params[param] = 20
            elif param == 'platform_side':  # platform_side is either 0 or 1
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


