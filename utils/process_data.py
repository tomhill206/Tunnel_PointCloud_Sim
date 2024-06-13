import pandas as pd
import numpy as np


def clean_csv(output_csv):
    # Read the CSV file into a DataFrame
    input_csv = '/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/csv/tunnel_frames_1_to_1.csv'
    df = pd.read_csv(input_csv, sep=';')

    # Define columns to keep
    columns_to_keep = [1, 6, 7, 8, 10]  # 0-indexed column numbers

    # Filter the DataFrame to keep only the specified columns
    df = df.iloc[:, columns_to_keep]

    # Rearrange columns - move first two columns to the end
    cols = df.columns.tolist()
    cols = cols[1:4] + [cols[4]] + [cols[0]]
    df = df[cols]

    # Set the values of the intensity column (column index 3) to zero
    df.iloc[:, 3] = 0

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv, sep=' ', index=False, header=False)

def remove_first_set_and_save(file_path):
    # Load the numpy array from the file
    params_array = np.load(file_path)

    # Check if the array is not empty
    if params_array.shape[0] > 0:
        # Remove the first set of parameters
        modified_array = params_array[1:]

        # Save the modified array back to the file
        np.save(file_path, modified_array)
    else:
        print("The file is empty or has only one set of parameters.")


#clean_csv('/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/pointclouds/tunnel1.csv')